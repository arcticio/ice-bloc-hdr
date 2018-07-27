

var gablog = {};

gablog.posts = {};
gablog.posts.confirmDeleteDiv = $("#post-delete-confirm");
gablog.posts.deleteErrorDiv = $("#post-delete-error");

gablog.posts.sending = false;

gablog.posts.http = {};
gablog.posts.dateField = $("#postDate");
gablog.dateFormat = "yyyy-mm-dd";

gablog.posts.handleDelete = function () {

  jQuery.ajax({
    type: "DELETE",
    url: gablog.posts.http.action,
    success: gablog.posts.handleSuccess,
    failure: gablog.posts.handleDeleteFailure
  });
  
};

gablog.posts.handleDeleteFailure = function (xhr, stat, err) {

  if (typeof (err) == "undefined") {
    $("#post-delete-error p").append("Error " + xhr.status + ": " + xhr.statusText);
  } else {
    $("#post-delete-error p").append("Error: " + err);
  }

  $("#post-delete-error").dialog({
    resizable: false,
    height: 145,
    modal: true,
    buttons: {
      "OK": function () {
        $("#post-delete-error").dialog("close");
      }
    }
  });

};

$(document).ready(function () {

  $("input#submit").click(function (e) {

    if (gablog.posts.sending){
      return eat(e);

    } else {
      gablog.posts.sending = true;
      if (gablog.posts.validate()){
        gablog.posts.handleSubmit();
      }
      setTimeout(function () {
        gablog.posts.sending = false;
      }, 1000)
      return eat(e);

    }
    
  });

  $("a#deletebtn").click(function (e) {
    e.preventDefault();
    gablog.posts.http = {};
    gablog.posts.http.action = $(e.target).attr("href");
    gablog.posts.http.verb = "DELETE";
    gablog.posts.confirmDeleteDiv.dialog("open");
  });

});

gablog.posts.handleFailure = function (xhr, stat, err) {

  if (typeof(err) == "undefined") {
    warning("Error " + xhr.status + ": " + xhr.statusText);

  } else {
    warning("Error: " + err);

  }
  
};

gablog.posts.validate = function () {

  if ($("#postTitle").val() == "") {
    alert("Please enter a title for this post.");
    return false;
  }

  if ($("#postBody").val() == "") {
    alert("Please enter a post");
    return false;
  }

  return true;

};

gablog.posts.handleSuccess = function (data, stat, xhr) {
  window.location.href = data;
};

gablog.posts.handleSubmit = function () {

  var postData = $("#postDialogForm").serialize(),
      payload;

  // console.log('postData', postData);

  postData += "&postBody="    + encodeURIComponent($("#postBody").val());
  postData += "&postExcerpt=" + encodeURIComponent($("#postExcerpt").val());

  if ($("form#postDialogForm").attr("action") != "") {
    console.log("TYP 0:", $("form#postDialogForm").attr("action"));
    gablog.posts.http.action = $("form#postDialogForm").attr("action") + "?_method=PUT";
    gablog.posts.http.verb = "POST";

  } else if ($("#newarticle").get(0).checked == true) {
    console.log("TYP 1: Article");
    gablog.posts.http.action = "/";
    gablog.posts.http.verb = "POST";

  } else {
    console.log("TYP 2: Blog, Post");
    var today = new Date();
    var month = today.getMonth() + 1;
    var year = today.getFullYear();
    gablog.posts.http.action = "/" + year + "/" + month;
    gablog.posts.http.verb = "POST";

  }

  payload = {
    type:     gablog.posts.http.verb,
    url:      gablog.posts.http.action.replace("//", "/"), // silly db bug once
    success:  gablog.posts.handleSuccess,
    error:    gablog.posts.handleFailure,
    // dataType: "text",
    data:     postData
  };

  // console.log(JSON.stringify(payload, null, 2));
  console.log("verb:", payload.type, "url:", payload.url, postData.length);

  // postData.split("&").forEach(function (token) {
  //   var t = token.split("=");
  //   if (t[0] !== 'postBody'){
  //    console.log(t[0], t[1]);
  //   }
  // });

  jQuery.ajax(payload);

};

gablog.posts.splitTags = function (val) {
  return val.split(/,/);
};
gablog.posts.extractLast = function (term) {
  return gablog.posts.splitTags(term).pop();
};

