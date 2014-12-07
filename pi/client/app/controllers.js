var eveApp = angular.module('eveApp', []);

eveApp.controller('EveCtrl', function ($scope, $http) {

  function refresh() {
    try {
      $http.get('/data.json').success(function(data) {
        $('#disconnected').hide();
        $scope.data = data;
        setTimeout(refresh, 100);
      }).
      error(function(data) {
        $('#disconnected').show();
        setTimeout(refresh, 1000);
      });
    } catch (e) {
    }
  }
  refresh();
  
  $scope.control = {
      motor0: {
        steps: 100,
        speed: 0,
        direction: 0
      },
      motor1: {
        steps: 100,
        speed: 0,
        direction: 0
      },
      motor2: {
        steps: 100,
        speed: 0,
        direction: 0
      }
  }
  
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
  
  $scope.submit_control = function() {
    var data = {
        motor0: {
          steps: parseInt($scope.control.motor0.steps),
          speed: parseInt($scope.control.motor0.speed),
          direction: parseInt($scope.control.motor0.direction)
        },
        motor1: {
          steps: parseInt($scope.control.motor1.steps),
          speed: parseInt($scope.control.motor1.speed),
          direction: parseInt($scope.control.motor1.direction)
        },
        motor2: {
          steps: parseInt($scope.control.motor2.steps),
          speed: parseInt($scope.control.motor2.speed),
          direction: parseInt($scope.control.motor2.direction)
        }
    }
    $http({
      url: '/control.json',
      method: "POST",
      data: data,
      headers: {'Content-Type': 'application/json'}
    });
  }
  
  $scope.submit_shutdown = function() {
    $http({
      url: '/shutdown.json',
      method: "POST",
      data: {},
      headers: {'Content-Type': 'application/json'}
    });
  }
});