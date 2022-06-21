/*
:author: riccardo mei
:encoding: utf-8
*/

const apiEndpoint = "http://127.0.0.1:5000";
const apiKey = "secret_psw";


function callApi(path, params, callback, async){
  /* If the API call fails, the callback function receives 'null' */
  const url = apiEndpoint + path;
  const req = new XMLHttpRequest();

  req.onload = () => {
    let data;
    if (req.status === 200){
      const response = req.responseText;
      data = JSON.parse(response);
    } else {
      console.log("status code =", req.status);
      data = null;
    }
    callback(data);
  }

  req.onerror = () => {
    console.log("Error...", url);
    callback(null);
  }

  req.open("POST", url, async);

  // The API awaits parameters
  const data = new FormData();
  data.append("data", JSON.stringify(params));
  data.append("apiKey", apiKey);

  req.send(data);
}


function testApi(){
    let inserted_id = null;
    function onApiResult(result) {
        console.log("API call result:");
        console.log(result);
    }

    const lista_chiamate = [
      ["/list", () => ({}), onApiResult],
      [
        "/insert",
        () => ({
          nome: "Marco", cognome: "Rossi", email: "ross@gmail.it", telefono: "3746598374"
        }),
        (apiResult) => {
          onApiResult(apiResult);
          inserted_id = apiResult['result'];
        }
      ],
      ["/list", () => ({}), onApiResult],
      [
        "/search",
        () => ({q : "Rossi"}),
        onApiResult
      ],
      [
        "/update",
        () => ({user_id: inserted_id, field_name: "nome", field_value: "value"}),
        onApiResult
      ],
      ["/list", () => ({}), onApiResult],
      [
        "/delete",
        () => ({user_id: inserted_id}),
        onApiResult
      ],
      ["/list", () => ({}), onApiResult]
    ];

    lista_chiamate.forEach((element_list) => {
        const path = element_list[0];
        const params = element_list[1]();
        const callback = element_list[2];

        console.log("---------------");
        console.log("PATH", path);
        console.log("PARAMS", params);
        console.log("CALLBACK", callback);

        callApi(path, params, callback, false);
        console.log("----------END----------");
    });
}
