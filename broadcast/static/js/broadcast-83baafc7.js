(function(window,$){"use strict";$('input[type="file"]').each(function(){var input=$(this),fileProxy=$('<a class="button small">Choose File</a>'),fileValue=$("<span>No file chosen</span>"),fileWrapper=$('<span class="file-wrapper"></span>');fileProxy.on("click",function(){input.click()});input.addClass("hidden");input.on("change",function(){fileValue.text($(this).val().split(/(\\|\/)/g).pop())});fileWrapper.append(fileProxy).append(fileValue);input.after(fileWrapper)});$("form").on("submit",function(){var form=$(this);form.find("button").attr("disabled","disabled");$(".progress-feedback").css("visibility","visible")})})(this,this.jQuery);