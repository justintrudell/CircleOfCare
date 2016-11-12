jQuery(document).ready(function () {

    $(document).on("click", '#edit-button', function () {
        $(this).attr('id', "save-button");
        $(this).find('span').text(" Save ");
        $(this).find('i').removeClass('fa-edit');
        $(this).find('i').addClass('fa-save');

        $(".edit").each(function () {
            $(this).removeClass('hidden');
        });

        $(".view").each(function () {
            $(this).addClass('hidden');
        });
    });

    $(document).on('click', '#save-button', function () {
        document.getElementById('profile-form').submit();
        $(this).attr('id', "edit-button");
        $(this).find('span').text(" Edit ");
        $(this).find('i').removeClass('fa-save');
        $(this).find('i').addClass('fa-edit');

        $(".edit").each(function () {
            $(this).addClass('hidden');
        });

        $(".view").each(function () {
            $(this).removeClass('hidden');
        });
    });
});
