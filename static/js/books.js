require(["jquery", "jquery-ui", "jquery-validate"], function($) {
  "use strict";

  var AVB = AVB || {};
  window.AVB = AVB;
  AVB.endlessMargin = 20;
  AVB.dialogOptions = {
    width: 700,
    modal: true,
    beforeClose: function() {
      $(this).empty();
    }
  };

  AVB.initTooltip = function() {
    if (!$(".tooltip").length) {
      return;
    }

    $(".tooltip").hover(
      function() {
        if($("aside", this)) {
          $("aside", this).show();
        }
      },
      function() {
        $("aside", this).hide();
      }
    );
  };

  AVB.init = function() {
    AVB.initTooltip();

    $("body").on("endless", function() {
      var $cont = $(this).find(".endless_container"), $ldr = $cont.find(".endless_loading"), $a = $cont.find("a");
      $ldr.show();
      var data = "querystring_key=" + $a.prop("rel").split(" ")[0];
      $.get($a.prop("href"), data, function(data) {
        $cont.before(data).remove();
      });
      return false;
    });

    var margin = 1;
    if (typeof AVB.endlessMargin !== "undefined") {
      margin = AVB.endlessMargin;
    }

    $(window).scroll(function(){
      var $win = $(window);
      if ($(document).height() - $win.height() - $win.scrollTop() <= margin) {
        $("body.homepage").trigger("endless");
        $(".homepage .tooltip").off("hover");
        AVB.initTooltip();
      }
    });

    $("body").on("click", "article.book", function(e) {
      var $this = $(this), id = $this.data("book-id") || $this.parents("article").data("book-id"), title = "",
          $me = $(e.target);

      if ($me.hasClass("aUpdateStatus")) {
        AVB.updateStatus(id, ($me.parents(".ui-dialog-content").length > 0));
        return false;
      }

      if ($me.hasClass("ui-icon-trash")) {
        AVB.deleteBook(id, ($me.parents(".ui-dialog-content").length > 0));
        return false;
      }

      if ($me.hasClass("author-link")) {
        AVB.showAuthor($me.prop("href"));
        return false;
      }

      title = $this.find("> a").prop("title");
      $.get("/book/"+id+"/", function(data) {

        if (typeof AVB.dialogOptions.open === "function") {
          delete AVB.dialogOptions.open;
        }
        AVB.openDialog(data, $.extend(AVB.dialogOptions, { title: title }));
      });
      return false;
    });

    $(".author-link").on("click", function(e) {
      var $me = $(e.target);
      AVB.showAuthor($me.prop("href"));
      return false;
    });

    $("#login").on("click", function(e) {
      e.preventDefault();
      $.get("/login", function(data) {
        AVB.openDialog(data, $.extend(AVB.dialogOptions, { title: "Login", width: 160 }));
      });
    });

    $('#addAuthor').on("click", function(e) {
      e.preventDefault();
      $.get("/author/add", function(data) {
         AVB.openDialog(data, $.extend(AVB.dialogOptions, { title: "Add New Author", width: 300 }));
      });
    });

    $("#addBook").on("click", function(e) {
      e.preventDefault();
      $.get("/book/add", function(data) {
        var options = {
          title: "Add New Book",
          width: 300,
          open: function() {
            var $form = $(this).find("form");
            $('#id_datefinished').datepicker({ dateFormat: 'yy-mm-dd' });

            $('#id_isbn').blur(function(){
              var isbn = $(this).val();
              var url = "https://www.googleapis.com/books/v1/volumes?callback=?&q="
              $.getJSON(url + isbn, function(response){
                var item = response.items[0];
                $('#id_title').val(item.volumeInfo.title);
                $('#id_pages').val(item.volumeInfo.pageCount);
                $('#id_amazon_link').val(item.volumeInfo.infoLink);
                $('#id_editorial').val(item.volumeInfo.description);
              });
            });

            $form.validate({
              rules: AVB.addBookFormRules
            });

            $(this).find(".btn-add-book").on("click", function() {
              $.ajax({
                url: $form.prop("action"),
                data: $form.serialize(),
                type: "post",
                cache: false,
                dataType: "html",
                contentType: false,
                processData: false,
                success: function () {
                  $("#dialog").data()["ui-dialog"].close();
                  window.location = "/";
                },
                error: AVB.Book.error
              });
            });
          }
        };
        AVB.openDialog(data, $.extend(AVB.dialogOptions, options));
      });
    });
  };

  AVB.updateStatus = function(id, isInDialog) {
    if (isInDialog) {
      $("#dialog").data()["ui-dialog"].close();
    }

    $.get("/book/"+id+"/update_status", function(data) {
      var options = {
        title: "Update Status",
        open: function() {
          AVB.Book.openUpdateStatus();
          var $form = $(this).find("form");
          $(this).find(".status-save").on("click", function() {
            $.ajax({
              url: $form.prop("action"),
              data: $form.serialize(),
              type: "post",
              cache: false,
              dataType: "html",
              success: function () {
                $("#dialog").data()["ui-dialog"].close();
                window.location = "/";
              },
              error: AVB.Book.error
            });
          });
        }
      };
      AVB.openDialog(data, $.extend(AVB.dialogOptions, options));
    });
  };

  AVB.deleteBook = function(id, isInDialog) {
    if (isInDialog) {
      $("#dialog").data()["ui-dialog"].close();
    }
    $.get("/book/"+id+"/delete", function(data) {
      var options = {
        title: "Delete Book",
        open: function() {
          var $this = $(this);
          $this.data()["ui-dialog"].element.append("Book has been deleted");
          $("body").find("[data-book-id='" + data.id + "']").fadeOut("slow").remove();
          setTimeout(function() {
            $this.data()["ui-dialog"].close();
          }, 1000);
        },
        bookId: data.id
      };
      if (typeof AVB.dialogOptions.open === "function") {
        delete AVB.dialogOptions.open;
      }
      AVB.openDialog(data, $.extend(AVB.dialogOptions, options));
    });
  };

  AVB.showAuthor = function(url) {
    var options = {
      title: "Author",
      open: function() {
        var $this = $(this);
        $this.data()["ui-dialog"].uiDialogTitlebar.find(".ui-dialog-title")
          .text($this.find(".authorBooks").data("author"));
      }
    };

    $.get(url, function(data) {
      AVB.openDialog(data, $.extend(AVB.dialogOptions, options));
    });
  };

  AVB.openDialog = function(data, options) {
    $("#dialog").empty().append(data).dialog(options);
  };

  AVB.Book = {
    message: null,
    book: null,
    objType: null,

    openUpdateStatus: function() {
      $("#id_status").change(function() {
        var $this = $(this);
        if ($this.val() === "1") {
          $this.next().show();
        } else {
          $this.next().hide();
        }
      });
    },

    init: function (bookId, objType) {
      var id = bookId;
      AVB.Book.objType = objType;

      $(".aAddToList").click( function (e) {
        e.preventDefault();
        $.get("/book/"+id+"/add_to_list", function() { });
      });

      $(".aUpdateOwn").click( function (e) {
        e.preventDefault();
        $.get("/book/"+id+"/update_own", function() { });
      });

      $(".aAddWebsite").click( function (e) {
        e.preventDefault();
        $.get("/author/"+id+"/add_website", function() { });
      });

      $(".aAddBio").click( function (e) {
        e.preventDefault();
        $.get("/author/"+id+"/add_bio", function() { });
      });

      $(".aAddWiki").click( function (e) {
        e.preventDefault();
        $.get("/author/"+id+"/add_wiki", function() { });
      });
    },

    show: function (id) {
      $("#status-container .status-save").click(function (e) {
        e.preventDefault();
        var msg = "", actionUrl = "";
        // validate form
        if (AVB.Book.validate()) {
          msg = $("#status-container .status-message");
          msg.fadeOut( function () {
            msg.removeClass("status-error").empty();
          });
          $("#status-container .status-title").text("Sending...");
          $("#status-container form").fadeOut(200);
          $("#status-container .status-content").animate({
            height: "80px"
          }, function () {
            $("#status-container .status-loading").fadeIn(200, function () {
              if (AVB.Book.objType === "author") {
                actionUrl = "/author/"+id+"/";
              } else {
                actionUrl = "/book/"+id+"/";
              }
              $.ajax({
                url: actionUrl,
                data: $("#status-container form").serialize() + "&action=send",
                type: "post",
                cache: false,
                dataType: "html",
                success: function () {
                  $("#status-container .status-loading").fadeOut(200, function () {
                    $("#status-container .status-title").text("Thank you!");
                  });
                },
                error: AVB.Book.error
              });
            });
          });
        } else {
          if ($("#status-container .status-message:visible").length > 0) {
            msg = $("#status-container .status-message div");
            msg.fadeOut(200, function () {
              msg.empty();
              AVB.Book.showError();
              msg.fadeIn(200);
            });
          } else {
            $("#status-container .status-message").animate({
              height: "30px"
            }, AVB.Book.showError);
          }

        }
      });
    },

    error: function (xhr) {
      console.log(xhr.statusText);
    },

    validate: function () {
      AVB.Book.message = "";
      if ($("#id_status").length) {
        if (!$("#status-container #id_status").val()) {
          AVB.Book.message += "Status is required. ";
        }
        if ($("#status-container #id_status").val() === "1") {
          if ($("#status-container #id_rating").val() === "0") {
            AVB.Book.message += "Rating is required. ";
          }

          if (!$("#status-container #id_datefinished").val()) {
            AVB.Book.message += "Date Finished is required. ";
          }

          if (!$("#status-container #id_review").val()) {
            AVB.Book.message += "Review is required.";
          }
        }
      } else if ($("#id_readinglist").length) {
        if (!$("#status-container #id_readinglist").val()) {
          AVB.Book.message += "Readinglist is required. ";
        }
      }

      return (AVB.Book.message.length) ? true : false;
    },
    showError: function () {
      $("#status-container .status-message")
        .html($("<div class=\"status-error\"></div>").append(AVB.Book.message))
        .fadeIn(200);
    }
  };


  function searchSubmit() {
    var query = encodeURIComponent($("#id_query").val());
    $("#search-results").load("/search/?ajax&query=" + query);
    return false;
  }

  function findTallest(element) {
    var tallest = 0, elHeight = 0;

    $(element).each(function () {
      elHeight = $(this).height();
      if (elHeight >= tallest) {
        tallest = elHeight;
      }
    });
    return tallest;
  }

  (function($,sr) {
    // debouncing function from John Hann
    // http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
    var debounce = function (func, threshold, execAsap) {
      var timeout;

      return function debounced () {
        var obj = this, args = arguments;

        function delayed () {
          if (!execAsap) {
            func.apply(obj, args);
          }
          timeout = null;
        }

        if (timeout) {
          clearTimeout(timeout);
        } else if (execAsap) {
          func.apply(obj, args);
        }

        timeout = setTimeout(delayed, threshold || 100);
      };
    };

    $.fn[sr] = function(fn){  return fn ? this.bind("resize", debounce(fn)) : this.trigger(sr); };

  })($,"smartresize");

  AVB.init();
});