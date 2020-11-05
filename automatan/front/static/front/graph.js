var labels = JSON.parse("{{js_lables|escapejs}}");
var data_price = JSON.parse("{{js_price|escapejs}}");
var name =
  "{{brand_name}}" + " " + "{{model_name}}" + " " + "{{year}}" + " " + "года";
var ctx = document.getElementById("myChart").getContext("2d");
var dataFirst = {
  label: name,
  backgroundColor: "rgba(255, 99, 132, 0.5)",
  borderColor: "rgba(255, 9, 13, 0.8)",
  data: data_price,
  order: 2,
};
var datasetList = [dataFirst];
console.log("{{ ses_var }}");

if ("{{ses_var}}" != "None") {
  console.log("{{ ses_var }}");
  var labels2 = JSON.parse("{{js_lables2|escapejs}}");
  var data_price2 = JSON.parse("{{js_price2|escapejs}}");
  var name2 = "{{brand_name2}}" + " " + "{{model_name2}}";

  var dataSecond = {
    label: name2,
    backgroundColor: "rgba(91, 196, 255, 0.5)",
    borderColor: "rgba(48, 132, 181, 0.8)",
    data: data_price2,
    order: 0,
  };
  datasetList = datasetList.concat(dataSecond);

  console.log("dataset_list_Second:", datasetList);
}

var chart = new Chart(ctx, {
  // The type of chart we want to create
  type: "line",
  // The data for our dataset
  data: {
    labels: labels,

    datasets: datasetList,
  },

  // Configuration options go here
  options: {},
});
