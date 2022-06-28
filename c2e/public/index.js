$( document ).ready(function() {
  $("#forward").click((e) => {
    doTheFetch("forward")
    $("img").addClass("forward");
    $("img").removeClass("backward");
  })
  $("#backward").click((e) => {
    doTheFetch("backward")
    $("img").removeClass("forward");
    $("img").addClass("backward");
  })
  $("#stop").click((e) => {
    doTheFetch("stop")
    $("img").removeClass("forward");
    $("img").removeClass("backward");
  })
  console.log( "ready!" );
});
const doTheFetch = (endpoint) => {
  fetch(`/${endpoint}`,{
    method: 'PUT',
    headers: { 'Content-Type':'application/json' },
    body: ""
  })
}
