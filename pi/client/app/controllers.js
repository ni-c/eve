var eveApp = angular.module('eveApp', []);

eveApp.controller('EveCtrl', function ($scope, $http) {

  function refresh() {
    $http.get('/data.json').success(function(data) {
      $scope.data = data;
	  setTimeout(refresh, 100);
    });
  }
  refresh();
  
  $scope.toggleRc = function() {
    $http({
      url: '/data.json',
      method: "POST",
      data: {'enabled': {'rc': $scope.data.enabled.rc}},
      headers: {'Content-Type': 'application/json'}
    });
  }
  
});