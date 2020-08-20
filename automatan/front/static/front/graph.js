// console.log('{{js_data|escapejs}}')
// var data = JSON.parse("{{js_data|escapejs}}")
var labels = JSON.parse("{{js_lables|escapejs}}");
var data_price = JSON.parse("{{js_price|escapejs}}");
var name = "{{brand_name}}" + "{{model_name}}";
var ctx = document.getElementById("myChart").getContext("2d");
var zalupka = {
  label: name,
  backgroundColor: "rgb(255, 99, 132)",
  borderColor: "rgb(255, 9, 13)",
  data: data_price,
};
console.log(data_price);
console.log(labels);

var chart = new Chart(ctx, {
  // The type of chart we want to create
  type: "line",
  // The data for our dataset
  data: {
    labels: labels,

    datasets: [
      zalupka,
      {
        label: "2009",
        backgroundColor: "rgb(25, 99, 132)",
        borderColor: "rgb(25, 9, 13)",
        data: ["3000000", "3000000"],
      },
    ],
  },

  // Configuration options go here
  options: {},
});
