var paddingBoxes = $('#schedule_results').find('.padding_box'),
    height0 = paddingBoxes.eq(0).innerHeight(),
    height1 = paddingBoxes.eq(1).innerHeight(),
    height2 = paddingBoxes.eq(2).innerHeight();

console.log(height1, height2);

if (height0 < height1) {
    paddingBoxes.eq(0).height(height1);
    paddingBoxes.eq(2).height(height1-70);
} else if (height1 < height0) {
    paddingBoxes.eq(1).height(height0);
    paddingBoxes.eq(2).height(height0-70);
}
