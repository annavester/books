(function($) {
    $(document).ready(function(){
        var margin = 1;
        if (typeof AVB.endless_on_scroll_margin != 'undefined') {
            margin = AVB.endless_on_scroll_margin;
        };
        $(window).scroll(function(){
	        var $win = $(window);
        	if ($(document).height() - $win.height() - $win.scrollTop() <= margin) {
        	    $("body").trigger("endless");
		        $('.tooltip').off('hover');
		        AVB.init_tooltip();
        	}
        });
    });
})(jQuery);