angular.module('myApp', []).controller('searcher', function($scope, $http) {
    $scope.query = "";
    $scope.query_title = "";
    $scope.query_limit = 200;
    $scope.total_results = -1;

    $scope.results = {};
    $scope.show_results = "false";
    $scope.remote_url = "http://curia.europa.eu/juris/document/document_print.jsf?doclang=IT&pageIndex=0&part=1&mode=req&docid=";

    $scope.search = function() {
        q = $scope.query;
        console.log("Query is: "+$scope.query);
        var url = "http://localhost:8500/search";
        var payload = {query: q, limit: $scope.query_limit};
//        console.log("Paylod is: "+payload)

        $http.post(url, payload) // ({method:"POST", url:"http://localhost:8500/search/"+q})
            .success(function(response) {
                console.log("Success!");
                $scope.query_title = response.query;
                $scope.results = response.data;
                $scope.total_results = response.total;
                if($scope.total_results < $scope.query_limit) {
                    $scope.message_result = "Showing " +$scope.total_results+ " hits out of " +$scope.total_results+" results";
                } else {
                    $scope.message_result = "Showing " +$scope.query_limit+ " hits out of " +$scope.total_results+" results";
                }
                $scope.show_results = "true";
            })
            .error(function(response) { console.log("Error!"); })
    };
});