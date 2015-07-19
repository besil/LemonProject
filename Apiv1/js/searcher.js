angular.module('myApp', []).controller('searcher', function($scope, $http) {
    $scope.query = "";
    $scope.query_title = "";
    $scope.results = {};

    $scope.search = function() {
        q = $scope.query;
        console.log("Query is: "+$scope.query);
//        $http.get("http://www.w3schools.com/angular/customers.php")
//        $http.get("localhost:8500/search/test")
//            .success(function(response) {$scope.results= response.records;});
        $http({method:"POST", url:"http://localhost:8500/search/"+q})
            .success(function(response) {
                console.log("Success!");
                console.log("response: "+response);
                x = response;
                console.log("response.data: "+response.data);
//                console.log("x: "+x)
//                console.log("x.data: "+x.data);
                $scope.query_title = response.query;
                $scope.results = response.data;
//                $scope.results= response.records;
//                var results = console.log(response.data);
//                $scope.results = [1,2,3];
//                console.log(results);
//                $scope.results = results;
            })
            .error(function(response) { console.log("Error!"); })
//        x = $http.get("localhost:8500/search/test");
//        console.log(x);
//        $scope.results = [1,2,3];
    };
});