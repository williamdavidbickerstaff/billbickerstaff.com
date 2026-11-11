---
title: sketchbooks
date: 10082076
order: 4
---

***Sketchbooks***

*Click on the corner of the pages to turn them*
<div id="book">
<div class="page">
<img src="../sketchbook/SketchbookScans/CoverFront.jpeg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_01.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_02.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_03.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_04.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_05.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_06.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_07.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_08.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_09.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_10.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_11.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_12.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_13.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_14.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_15.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_16.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_17.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_18.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_19.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_20.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_21.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_22.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_23.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_24.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_25.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_26.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_27.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_28.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_29.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_30.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_31.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_32.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_33.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_34.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_35.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_36.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_37.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_38.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_39.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_40.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_41.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/scan_42.jpg" />
</div>
<div class="page">
<img src="../sketchbook/SketchbookScans/CoverBack.jpeg" />
</div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/4.0.0/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/turn.js/3/turn.min.js"></script>

<script>
$(function () {
  const book = $("#book");

  function resizeBook() {
    const width = book.parent().width();
    const image = book.find("img").first()[0];

    if (!image.naturalWidth) return;

    // The book contains two pages side by side.
    const pageWidth = width / 2;
    const height = pageWidth * image.naturalHeight / image.naturalWidth;

    book.turn("size", width, height);
  }

  book.turn({
    width: book.parent().width(),
    height: 850,
    autoCenter: true,
    gradients: true,
    acceleration: true
  });

  book.find("img").first().on("load", resizeBook);
  $(window).on("resize", resizeBook);

  resizeBook();
});
</script>

When I draw, it is often absent mindedly. Sometimes more descriptive, other times a bare minimum. I know that I have found a good drawing when I have found a good shape, a simple shape that can be drawn without thinking too much. A shape that seems to capture something about my subject that is true and simple, but also unexpected. I don’t find this very often, but when I do, I will draw it regularly for years. It has been added to my collection.