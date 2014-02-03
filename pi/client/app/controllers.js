var eveApp = angular.module('eveApp', []);

eveApp.controller('EveCtrl', function ($scope, $http) {
  function refresh() {
    $http.get('/data.json').success(function(data) {
      $scope.data = data;
    });
  }
  
  setInterval(refresh, 100);
  
});