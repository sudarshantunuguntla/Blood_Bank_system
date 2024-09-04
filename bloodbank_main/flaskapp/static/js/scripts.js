$("form[name=signup_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/dashboard/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=edit_profile_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();
  // setTimeout(function(){
  //   alert("I am setTimeout");
  // },1000000000000000);
  // console.log("loginprocess")
  $.ajax({
    url: "/user/editprof",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/profile";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});




$("form[name=login_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();
  // setTimeout(function(){
  //   alert("I am setTimeout");
  // },1000000000000000);
  // console.log("loginprocess")

  $.ajax({
    url: "/user/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/dashboard/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

document.getElementById("nextBtn").addEventListener("click", function() {
  // Get all images
  var images = document.querySelectorAll(".photos img");
  var visibleIndex = -1;

  // Find the index of the currently visible image
  for (var i = 0; i < images.length; i++) {
      if (!images[i].classList.contains("hidden")) {
          visibleIndex = i;
          break;
      }
  }

  // Toggle visibility of the current and next images
  if (visibleIndex !== -1) {
      images[visibleIndex].classList.add("hidden");
      var nextIndex = (visibleIndex + 1) % images.length;
      images[nextIndex].classList.remove("hidden");
  }
});