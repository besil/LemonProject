angular.module('myApp', []).controller('searcher', function($scope, $http) {
    $scope.query = "";
    $scope.query_title = "";
    $scope.results = {};
    $scope.show_results = "false";
    $scope.remote_url = "http://curia.europa.eu/juris/document/document_print.jsf?doclang=IT&pageIndex=0&part=1&mode=req&docid=";

    $scope.search = function() {
        q = $scope.query;
        console.log("Query is: "+$scope.query);
        var url = "http://localhost:8500/search";
        var payload = {query: q};
//        console.log("Paylod is: "+payload)

        $http.post(url, payload) // ({method:"POST", url:"http://localhost:8500/search/"+q})
            .success(function(response) {
                console.log("Success!");
//                console.log("response.query: "+response.query);
//                console.log("response.data: "+response.data);

                $scope.query_title = response.query;
                $scope.results = response.data;
                $scope.show_results = "true";
            })
            .error(function(response) { console.log("Error!"); })
    };
});