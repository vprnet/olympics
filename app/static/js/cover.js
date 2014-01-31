var photo = window.top.document.getElementById('cover_photo'),
    bigScreenH2  = window.top.document.getElementById('big_screen_h2'),
    smallScreenH2 = window.top.document.getElementById('small_screen_h2'),
    photoCredit = window.top.document.getElementById('photo_credit'),
    navbar = window.top.document.getElementsByClassName('navbar')[0];

    bigScreenH2.style.maxHeight = (window.innerHeight - navbar.offsetHeight) + 'px';
    photoCredit.style.maxHeight = (window.innerHeight - navbar.offsetHeight) + 'px';
if ((photo.offsetHeight + navbar.offsetHeight + 20) < window.innerHeight) {
    bigScreenH2.style.display = 'none';
    smallScreenH2.style.display = 'block';
} else {
    console.log(photo.offsetHeight + 'px;');
}
