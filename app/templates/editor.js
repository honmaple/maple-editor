$(function() {
    var cursorPosition = {
        get: function (textarea) {
            var rangeData = {text: "", start: 0, end: 0 };
            if (textarea.setSelectionRange) { // W3C
                textarea.focus();
                rangeData.start= textarea.selectionStart;
                rangeData.end = textarea.selectionEnd;
                rangeData.text = (rangeData.start != rangeData.end) ? textarea.value.substring(rangeData.start, rangeData.end): "";
            } else if (document.selection) { // IE
                textarea.focus();
                var i,
                oS = document.selection.createRange(),
                    oR = document.body.createTextRange();
                    oR.moveToElementText(textarea);
                    rangeData.text = oS.text;
                    rangeData.bookmark = oS.getBookmark();
                    for (i = 0; oR.compareEndPoints('StartToStart', oS) < 0 && oS.moveStart("character", -1) !== 0; i ++) {

                        if (textarea.value.charAt(i) == '\r' ) {
                            i ++;
                        }
                    }
                    rangeData.start = i;
                    rangeData.end = rangeData.text.length + rangeData.start;
            }
            return rangeData;
        }
    };
    function loadFile(event) {
        var reader = new FileReader();
        reader.onload = function(){
            $("#output").attr('src',reader.result);
        };
        reader.readAsDataURL(event.target.files[0]);
    };
    function preview(){
        $.post("{{ url_for('question.preview') }}", {
            content: $("#content").val(),
            choice: $("#choice").val()
        }, function(data) {
            $("#showPreview").html(data);
        });
    }
    $('a#editor-a').click(function() {
        var tx = $("#content")[0];
        var result;
        var text = "文本";
        var oValue,nValue;
        result = cursorPosition.get(tx);
        text = '<a href="'+ result.text +  '" title="">'+'</a>';
        oValue = $("#content").val();
        nValue = oValue.substring(0, result.start) + text + oValue.substring(result.end);
        $("#content").val(nValue);
    });
    $('a#editor-b').click(function() {
        var tx = $("#content")[0];
        var result;
        var text = "文本";
        var oValue,nValue;
        result = cursorPosition.get(tx);
        text = '<b>' + result.text + '</b>';
        oValue = $("#content").val();
        nValue = oValue.substring(0, result.start) + text + oValue.substring(result.end);
        $("#content").val(nValue);
    });
    $('a#editor-i').click(function() {
        var tx = $("#content")[0];
        var result;
        var text = "文本";
        var oValue,nValue;
        result = cursorPosition.get(tx);
        text = '<i>' + result.text + '</i>';
        oValue = $("#content").val();
        nValue = oValue.substring(0, result.start) + text + oValue.substring(result.end);
        $("#content").val(nValue);
    });
    $('a#editor-bq').click(function() {
        var tx = $("#content")[0];
        var result;
        var text = "文本";
        var oValue,nValue;
        result = cursorPosition.get(tx);
        text = '<blockquote>' + result.text + '</blockquote>';
        oValue = $("#content").val();
        nValue = oValue.substring(0, result.start) + text + oValue.substring(result.end);
        $("#content").val(nValue);
    });
    $('a#editor-c').click(function() {
        var tx = $("#content")[0];
        var result;
        var text = "文本";
        var oValue,nValue;
        result = cursorPosition.get(tx);
        text = '<pre>' + result.text + '</pre>';
        oValue = $("#content").val();
        nValue = oValue.substring(0, result.start) + text + oValue.substring(result.end);
        $("#content").val(nValue);
    });
    $('a#editor-h').click(function() {
        var tx = $("#content")[0];
        var result;
        var text;
        var oValue,nValue;
        result = cursorPosition.get(tx);
        text = '<h3>' + result.text + '</h3>';
        oValue = $("#content").val();
        nValue = oValue.substring(0, result.start) + text + oValue.substring(result.end);
        $("#content").val(nValue);
    });
    $('a#editor-hr').click(function() {
        var text = $("#content").val();
        $("#content").val(text + '<hr>');
    });
    $('button#uploadFile').click(function() {
        var formData = new FormData($('#uploadForm')[0]);
        var content=$("#content").val();
        alert(formData);
        $.ajax({
            type: 'POST',
            url: '/question/uploads',
            data: formData,
            contentType: false,
            processData: false,
            dataType: 'json',
            error: function(data){
                alert(data.error);
            },
            success: function(result) {
                if (result.judge == true)
                    {
                        var img_url = '<img src="' +'/question/uploads/' + result.error + '" alt="photo">';
                        $("#content").val(content+img_url);
                    }
                else
                    {
                        alert(result.error);
                    };
            },
        });
    });
}
