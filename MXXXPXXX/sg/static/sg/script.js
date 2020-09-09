// 2.  글쓰기 페이지

// 이미지 첨부시 미리보기

function setThumbnail(event) {
  var reader = new FileReader();

  reader.onload = function (event) {
    var img = document.createElement("img");
    img.setAttribute("src", event.target.result);
    document.querySelector("div#image_container").appendChild(img);
  };

  reader.readAsDataURL(event.target.files[0]);
}

//제목 단어 추천

function recommendTitle(val, csrf_token) {
  $.ajax({
    type: "POST",
    url: "recommend/",
    data: { 'content': val, 'csrfmiddlewaretoken': csrf_token },
    dataType: "json",
    success: function (response) {
      var recommend = response.recommend;
      var res1 = recommend[0];
      var res2 = recommend[1];
      var res3 = recommend[2];
      var res4 = recommend[3];
      var res5 = recommend[4];

      if (val == "") {
        document.getElementById('result').value = "0";
      } else {
        document.getElementById('result1').value = res1;
        document.getElementById('result2').value = res2;
        document.getElementById('result3').value = res3;
        document.getElementById('result4').value = res4;
        document.getElementById('result5').value = res5;
      }
    }
  });
}

function addTitle(val, csrf_token) {
  var new_title = document.getElementById('title').value + val;
  document.getElementById('title').value = new_title;
  recommendTitle(new_title, csrf_token);
}

//이미지 클릭시 자동 넣기

function mark(img) {
  img.style.border = "1px solid blue";
}