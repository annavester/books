var Book = {
    message: null,
    book: null,
    obj_type: null,
    
    init: function (book_id, obj_type) {
        book = book_id;
        Book.obj_type = obj_type;
        $('.aUpdateStatus').click( function (e) {
            e.preventDefault();

            // load the Book form using ajax
            $.get("/book/"+book+"/update_status", function(data) {
                // create a modal dialog with the data
                $(data).modal({
                    closeHTML: "<a href='#' title='Close' class='modal-close'>x</a>",
                    position: ["15%",],
                    overlayId: 'modal-overlay',
                    containerId: 'status-container',
                    onOpen: Book.open,
                    onShow: Book.show,
                    onClose: Book.close
                });
            });
        });
        
        
        $('.aAddToList').click( function (e) {
            e.preventDefault();

            // load the Book form using ajax
            $.get("/book/"+book+"/add_to_list", function(data) {
                // create a modal dialog with the data
                $(data).modal({
                    closeHTML: "<a href='#' title='Close' class='modal-close'>x</a>",
                    position: ["15%",],
                    overlayId: 'modal-overlay',
                    containerId: 'status-container',
                    onOpen: Book.open,
                    onShow: Book.show,
                    onClose: Book.close
                });
            });
        });
        
        $('.aUpdateOwn').click( function (e) {
            e.preventDefault();

            // load the Book form using ajax
            $.get("/book/"+book+"/update_own", function(data) {
                // create a modal dialog with the data
                $(data).modal({
                    closeHTML: "<a href='#' title='Close' class='modal-close'>x</a>",
                    position: ["15%",],
                    overlayId: 'modal-overlay',
                    containerId: 'status-container',
                    onOpen: Book.open,
                    onShow: Book.show,
                    onClose: Book.close
                });
            });
        });
        
        $('.aAddWebsite').click( function (e) {
            e.preventDefault();

            // load the Book form using ajax
            $.get("/author/"+book+"/add_website", function(data) {
                // create a modal dialog with the data
                $(data).modal({
                    closeHTML: "<a href='#' title='Close' class='modal-close'>x</a>",
                    position: ["15%",],
                    overlayId: 'modal-overlay',
                    containerId: 'status-container',
                    onOpen: Book.open,
                    onShow: Book.show,
                    onClose: Book.close
                });
            });
        });
        
        $('.aAddBio').click( function (e) {
            e.preventDefault();

            // load the Book form using ajax
            $.get("/author/"+book+"/add_bio", function(data) {
                // create a modal dialog with the data
                $(data).modal({
                    closeHTML: "<a href='#' title='Close' class='modal-close'>x</a>",
                    position: ["15%",],
                    overlayId: 'modal-overlay',
                    containerId: 'status-container',
                    onOpen: Book.open,
                    onShow: Book.show,
                    onClose: Book.close
                });
            });
        });
        
        $('.aAddWiki').click( function (e) {
            e.preventDefault();

            // load the Book form using ajax
            $.get("/author/"+book+"/add_wiki", function(data) {
                // create a modal dialog with the data
                $(data).modal({
                    closeHTML: "<a href='#' title='Close' class='modal-close'>x</a>",
                    position: ["15%",],
                    overlayId: 'modal-overlay',
                    containerId: 'status-container',
                    onOpen: Book.open,
                    onShow: Book.show,
                    onClose: Book.close
                });
            });
        });
    },
    open: function (dialog) {
        // add padding to the buttons in firefox/mozilla
        if ($.browser.mozilla) {
            $('#status-container .status-button').css({
                'padding-bottom': '2px'
            });
        }
        // input field font size
        if ($.browser.safari) {
            $('#status-container .status-input').css({
                'font-size': '.9em'
            });
        }

        // dynamically determine height
        var h = 280;

        var title = $('#status-container .status-title').html();
        $('#status-container .status-title').html('Loading...');
        dialog.overlay.fadeIn(200, function () {
            dialog.container.fadeIn(200, function () {
                dialog.data.fadeIn(200, function () {
                    $('#status-container .status-content').animate({
                        height: h
                    }, function () {
                        $('#status-container .status-title').html(title);
                        $('#status-container form').fadeIn(200, function () {
                            $('#status-container #id_status').focus();

                            $('#id_status').change(function() {
                                if ($('#id_status').val() == 1) {
                                    $('#status-container .divHaveRead').show();
                                } else {                                        
                                    $('#status-container .divHaveRead').hide();
                                }
                            });
                        });
                    });
                });
            });
        });
    },
    show: function (dialog) {
        $('#status-container .status-save').click( function (e) {
            e.preventDefault();
            // validate form
            if (Book.validate()) {
                var msg = $('#status-container .status-message');
                msg.fadeOut( function () {
                    msg.removeClass('status-error').empty();
                });
                $('#status-container .status-title').html('Sending...');
                $('#status-container form').fadeOut(200);
                $('#status-container .status-content').animate({
                    height: '80px'
                }, function () {
                    $('#status-container .status-loading').fadeIn(200, function () {
                        if (Book.obj_type == "author") {                            
                            actionUrl = '/author/'+book+'/';
                        } else {
                            actionUrl = '/book/'+book+'/';
                        }
                        $.ajax({
                            url: actionUrl,
                            data: $('#status-container form').serialize() + '&action=send',
                            type: 'post',
                            cache: false,
                            dataType: 'html',
                            success: function (data) {
                                $('#status-container .status-loading').fadeOut(200, function () {
                                    $('#status-container .status-title').html('Thank you!');
                                });
                            },
                            error: Book.error
                        });
                    });
                });
            } else {
                if ($('#status-container .status-message:visible').length > 0) {
                    var msg = $('#status-container .status-message div');
                    msg.fadeOut(200, function () {
                        msg.empty();
                        Book.showError();
                        msg.fadeIn(200);
                    });
                } else {
                    $('#status-container .status-message').animate({
                        height: '30px'
                    }, Book.showError);
                }

            }
        });
    },
    close: function (dialog) {
        $('#status-container .status-message').fadeOut();
        $('#status-container .status-title').html('Goodbye...');
        $('#status-container form').fadeOut(200);
        $('#status-container .status-content').animate({
            height: 40
        }, function () {
            dialog.data.fadeOut(200, function () {
                dialog.container.fadeOut(200, function () {
                    dialog.overlay.fadeOut(200, function () {
                        $.modal.close();
                    });
                });
            });
        });
    },
    error: function (xhr) {
        alert(xhr.statusText);
    },
    validate: function () {
        Book.message = '';
        if ($('#id_status').length != 0) {
            if (!$('#status-container #id_status').val()) {
                Book.message += 'Status is required. ';
            }
            if ($('#status-container #id_status').val()==1) {
                if ($('#status-container #id_rating').val()==0) {
                    Book.message += 'Rating is required. ';
                }
    
                if (!$('#status-container #id_datefinished').val()) {
                    Book.message += 'Date Finished is required. ';
                }
    
                if (!$('#status-container #id_review').val()) {
                    Book.message += 'Review is required.';
                }
            }
        } else if ($('#id_readinglist').length != 0) {
            if (!$('#status-container #id_readinglist').val()) {
                Book.message += 'Readinglist is required. ';
            }
        }

        if (Book.message.length > 0) {
            return false;
        } else {
            return true;
        }
    },
    showError: function () {
        $('#status-container .status-message')
        .html($('<div class="status-error"></div>').append(Book.message))
        .fadeIn(200);
    }
};

var AVB = AVB || {};
AVB.endless_on_scroll_margin = 20;

AVB.init_tooltip = function(){
	if (!$('.tooltip').length) {
		return;
	}

	$('.tooltip').hover(
		function() {
			if($('aside', this)) {
				$('aside', this).show();
			}
		},
		function() {
			$('aside', this).hide();
		}
	);
};


function search_submit() {
    var query = $('#id_query').val();
    $('#search-results').load(
        "/search/?ajax&query=" + encodeURIComponent(query)
    );
    return false;
}
function findTallest(element) {            
    var tallest = 0;
    var elHeight = 0;
    $(element).each(function (index) {
        elHeight = $(this).height();        
        if (elHeight >= tallest) {
            tallest = elHeight;
        }
    });
    return tallest;
}

(function($,sr){
 
  // debouncing function from John Hann
  // http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
  var debounce = function (func, threshold, execAsap) {
      var timeout;
 
      return function debounced () {
          var obj = this, args = arguments;
          function delayed () {
              if (!execAsap)
                  func.apply(obj, args);
              timeout = null; 
          };
 
          if (timeout)
              clearTimeout(timeout);
          else if (execAsap)
              func.apply(obj, args);
 
          timeout = setTimeout(delayed, threshold || 100); 
      };
  }
	// smartresize 
	jQuery.fn[sr] = function(fn){  return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr); };
 
})(jQuery,'smartresize');
