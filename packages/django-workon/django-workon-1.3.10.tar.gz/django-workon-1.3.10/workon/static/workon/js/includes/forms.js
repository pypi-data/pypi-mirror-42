(function ($, modalFormSelector, formSelector, isDict, isArray)
{
    $(document).ready(function()
    {


          var input_selector = 'input[type=text], input[type=password], input[type=email], input[type=url], input[type=tel], input[type=number], input[type=search], textarea';
          $(document).on('change', input_selector, function ()
          {
              if($(this).val().length !== 0 || $(this).attr('placeholder') !== undefined)
              {
                  $(this).siblings('label').addClass('active');
              }
              //validate_field($(this));
          });
          // $(document).on('click', '[type="checkbox"]+label', function ()
          // {

          // });

       $('select:not(.django-select2)').material_select();


      // Function to update labels of text fields
      Materialize.updateTextFields = function() {
        var input_selector = 'input[type=text], input[type=password], input[type=email], input[type=url], input[type=tel], input[type=number], input[type=search], textarea';
        $(input_selector).each(function(index, element) {
          var $this = $(this);
          if ($(element).val().length > 0 || element.autofocus || $this.attr('placeholder') !== undefined) {
            $this.siblings('label').addClass('active');
          } else if ($(element)[0].validity) {
            $this.siblings('label').toggleClass('active', $(element)[0].validity.badInput === true);
          } else {
            $this.siblings('label').removeClass('active');
          }
        });
      };

      // Text based inputs
      var input_selector = 'input[type=text], input[type=password], input[type=email], input[type=url], input[type=tel], input[type=number], input[type=search], textarea';

      // Add active if form auto complete
      $(document).on('change', input_selector, function () {
        if($(this).val().length !== 0 || $(this).attr('placeholder') !== undefined) {
          $(this).siblings('label').addClass('active');
        }
        validate_field($(this));
      });

      // Add active if input element has been pre-populated on document ready
      $(document).ready(function() {
        Materialize.updateTextFields();
      });

      // HTML DOM FORM RESET handling
      $(document).on('reset', function(e) {
        var formReset = $(e.target);
        if (formReset.is('form')) {
          formReset.find(input_selector).removeClass('valid').removeClass('invalid');
          formReset.find(input_selector).each(function () {
            if ($(this).attr('value') === '') {
              $(this).siblings('label').removeClass('active');
            }
          });

          // Reset select
          formReset.find('select.initialized').each(function () {
            var reset_text = formReset.find('option[selected]').text();
            formReset.siblings('input.select-dropdown').val(reset_text);
          });
        }
      });

      // Add active when element has focus
      $(document).on('focus', input_selector, function () {
        $(this).siblings('label, .prefix').addClass('active');
      });

      $(document).on('blur', input_selector, function () {
        var $inputElement = $(this);
        var selector = ".prefix";

        if ($inputElement.val().length === 0 && $inputElement[0].validity.badInput !== true && $inputElement.attr('placeholder') === undefined) {
          selector += ", label";
        }

        $inputElement.siblings(selector).removeClass('active');

        validate_field($inputElement);
      });

      window.validate_field = function(object) {
        var hasLength = object.attr('data-length') !== undefined;
        var lenAttr = parseInt(object.attr('data-length'));
        var len = object.val().length;

        if (object.val().length === 0 && object[0].validity.badInput === false) {
          if (object.hasClass('validate')) {
            object.removeClass('valid');
            object.removeClass('invalid');
          }
        }
        else {
          if (object.hasClass('validate')) {
            // Check for character counter attributes
            if ((object.is(':valid') && hasLength && (len <= lenAttr)) || (object.is(':valid') && !hasLength)) {
              object.removeClass('invalid');
              object.addClass('valid');
            }
            else {
              object.removeClass('valid');
              object.addClass('invalid');
            }
          }
        }
      };

      // Radio and Checkbox focus class
      var radio_checkbox = 'input[type=radio], input[type=checkbox]';
      $(document).on('keyup.radio', radio_checkbox, function(e) {
        // TAB, check if tabbing to radio or checkbox.
        if (e.which === 9) {
          $(this).addClass('tabbed');
          var $this = $(this);
          $this.one('blur', function(e) {

            $(this).removeClass('tabbed');
          });
          return;
        }
      });



      // File Input Path
      $(document).on('change', '.file-field input[type="file"]', function () {
        var file_field = $(this).closest('.file-field');
        var path_input = file_field.find('input.file-path');
        var files      = $(this)[0].files;
        var file_names = [];
        for (var i = 0; i < files.length; i++) {
          file_names.push(files[i].name);
        }
        path_input.val(file_names.join(", "));
        path_input.trigger('change');
      });

      /****************
      *  Range Input  *
      ****************/

      var range_type = 'input[type=range]';
      var range_mousedown = false;
      var left;

      $(range_type).each(function () {
        var thumb = $('<span class="thumb"><span class="value"></span></span>');
        $(this).after(thumb);
      });

      var showRangeBubble = function(thumb) {
        var paddingLeft = parseInt(thumb.parent().css('padding-left'));
        var marginLeft = (-7 + paddingLeft) + 'px';
        thumb.velocity({ height: "30px", width: "30px", top: "-30px", marginLeft: marginLeft}, { duration: 300, easing: 'easeOutExpo' });
      };

      var calcRangeOffset = function(range) {
        var width = range.width() - 15;
        var max = parseFloat(range.attr('max'));
        var min = parseFloat(range.attr('min'));
        var percent = (parseFloat(range.val()) - min) / (max - min);
        return percent * width;
      }

      var range_wrapper = '.range-field';
      $(document).on('change', range_type, function(e) {
        var thumb = $(this).siblings('.thumb');
        thumb.find('.value').html($(this).val());

        if (!thumb.hasClass('active')) {
          showRangeBubble(thumb);
        }

        var offsetLeft = calcRangeOffset($(this));
        thumb.addClass('active').css('left', offsetLeft);
      });

      $(document).on('mousedown touchstart', range_type, function(e) {
        var thumb = $(this).siblings('.thumb');

        // If thumb indicator does not exist yet, create it
        if (thumb.length <= 0) {
          thumb = $('<span class="thumb"><span class="value"></span></span>');
          $(this).after(thumb);
        }

        // Set indicator value
        thumb.find('.value').html($(this).val());

        range_mousedown = true;
        $(this).addClass('active');

        if (!thumb.hasClass('active')) {
          showRangeBubble(thumb);
        }

        if (e.type !== 'input') {
          var offsetLeft = calcRangeOffset($(this));
          thumb.addClass('active').css('left', offsetLeft);
        }
      });

      $(document).on('mouseup touchend', range_wrapper, function() {
        range_mousedown = false;
        $(this).removeClass('active');
      });

      $(document).on('input mousemove touchmove', range_wrapper, function(e) {
        var thumb = $(this).children('.thumb');
        var left;
        var input = $(this).find(range_type);

        if (range_mousedown) {
          if (!thumb.hasClass('active')) {
            showRangeBubble(thumb);
          }

          var offsetLeft = calcRangeOffset(input);
          thumb.addClass('active').css('left', offsetLeft);
          thumb.find('.value').html(thumb.siblings(range_type).val());
        }
      });

      $(document).on('mouseout touchleave', range_wrapper, function() {
        if (!range_mousedown) {

          var thumb = $(this).children('.thumb');
          var paddingLeft = parseInt($(this).css('padding-left'));
          var marginLeft = (7 + paddingLeft) + 'px';

          if (thumb.hasClass('active')) {
            thumb.velocity({ height: '0', width: '0', top: '10px', marginLeft: marginLeft}, { duration: 100 });
          }
          thumb.removeClass('active');
        }
      });
      

    }); // End of $(document).ready

    /*******************
     *  Select Plugin  *
     ******************/

  $.fn.material_select = function (callback) {
    $(this).each(function(){
      $(this).select2();
      return;
    });
  };

}( jQuery ));
