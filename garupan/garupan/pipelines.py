# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import hashlib
from io import BytesIO

# useful for handling different item types with a single interface
from itemadapter.adapter import ItemAdapter
from PIL.PngImagePlugin import PngInfo
from scrapy.pipelines.files import _md5sum
from scrapy.pipelines.images import ImageException, ImagesPipeline
from scrapy.utils.python import to_bytes


class GarupanPipeline(ImagesPipeline):
    def image_downloaded(self, response, request, info, *, item=None):
        checksum = None
        for path, image, buf in self.get_images(response, request, info, item=item):
            if checksum is None:
                buf.seek(0)
                checksum = _md5sum(buf)
            width, height = image.size
            self.store.persist_file(
                path,
                buf,
                info,
                meta={"width": width, "height": height},
                headers={"Content-Type": "image/png"},  # 此处改为保存 png 图片
            )
        assert checksum is not None
        return checksum

    def get_images(self, response, request, info, *, item=None):
        path = self.file_path(request, response=response, info=info, item=item)
        orig_image = self._Image.open(BytesIO(response.body))

        width, height = orig_image.size
        if width < self.min_width or height < self.min_height:
            raise ImageException(
                "Image too small "
                f"({width}x{height} < "
                f"{self.min_width}x{self.min_height})"
            )

        image, buf = self.convert_image(
            orig_image, response_body=BytesIO(response.body), item=item
        )
        yield path, image, buf

    # 传入 item 参数
    def convert_image(self, image, size=None, *, response_body, item):
        # 添加服饰名称到注释
        metadata = PngInfo()
        # for k, v in image.text.items():
        #     metadata.add_text(k, v)
        metadata.add_text("comment", ItemAdapter(item).get("description", ""))
        buf = BytesIO()
        image.save(buf, "PNG", pnginfo=metadata)
        return image, buf

    def file_path(self, request, response=None, info=None, *, item):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        name = ItemAdapter(item).get("name")
        return f"{name}/{image_guid}.png"
