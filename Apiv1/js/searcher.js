angular.module('myApp', []).controller('searcher', function($scope, $http) {
    $scope.query = "";
    $scope.query_title = "";
    $scope.results = {};
    $scope.show_results = "false";

    $scope.search = function() {
        q = $scope.query;
        console.log("Query is: "+$scope.query);

        $http({method:"POST", url:"http://localhost:8500/search/"+q})
            .success(function(response) {
                console.log("Success!");
                console.log("response.query: "+response.query);
                console.log("response.data: "+response.data);

                $scope.query_title = response.query;
                $scope.results = response.data;
                $scope.show_results = "true";
            })
            .error(function(response) { console.log("Error!"); })
    };
});