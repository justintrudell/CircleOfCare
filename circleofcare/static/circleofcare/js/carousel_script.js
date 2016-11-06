$('#carousel').on('slide.bs.carousel', function (ev) {
    var id = ev.relatedTarget.id;
    if (id == 'second-slide') {
        document.getElementById("next-arrow").className = 'right carousel-control hidden';
        document.getElementById("submit-check").className = 'right carousel-control';
        document.getElementById("prev-arrow").className = 'left carousel-control';
    }
    else if (id == 'first-slide') {
        document.getElementById("submit-check").className = 'right carousel-control hidden';
        document.getElementById("next-arrow").className = 'right carousel-control';
        document.getElementById("prev-arrow").className = 'left carousel-control hidden';
    }
});