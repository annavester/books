(function($) {
    $(document).ready(function(){
        $("body").on("endless", function() {
            var $cont = $(this).find(".endless_container"), $ldr = $cont.find(".endless_loading"), $a = $cont.find("a");
            $ldr.show();
            var data = "querystring_key=" + $a.prop("rel").split(" ")[0];
            $.get($a.prop("href"), data, function(data) {
                $cont.before(data).remove();
            });
            return false;
        });
    });
})(jQuery);