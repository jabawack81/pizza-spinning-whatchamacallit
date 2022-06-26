$( document ).ready(function() {
  $("#forward").click((e) => doTheFetch("forward") )
  $("#backward").click((e) => doTheFetch("backward") )
  $("#stop").click((e) => doTheFetch("stop") )
  console.log( "ready!" );
});
const doTheFetch = (endpoint) => {
  fetch(`/${endpoint}`,{
    method: 'PUT',
    headers: { 'Content-Type':'application/json' },
    body: ""
  })
}
