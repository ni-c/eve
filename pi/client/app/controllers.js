var eveApp = angular.module('eveApp', []);

eveApp.controller('EveCtrl', function ($scope, $http) {

  function refresh() {
    try {
      $http.get('/data.json').success(function(data) {
        $('#disconnected').hide();
        $scope.data = data;
        setTimeout(refresh, 500);
      }).
      error(function(data) {
        $('#disconnected').show();
        setTimeout(refresh, 1000);
      });
    } catch (e) {
    }
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
  
  $scope.toggleMotor = function() {
    $http({
      url: '/data.json',
      method: "POST",
      data: {'enabled': {'motor': $scope.data.enabled.motor}},
      headers: {'Content-Type': 'application/json'}
    });
  }
  
});