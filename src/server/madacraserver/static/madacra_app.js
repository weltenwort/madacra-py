var app,__slice=[].slice;app=angular.module("madacra",["madacra.identity","madacra.campaign"]);app.config(function($interpolateProvider,$routeProvider){$interpolateProvider.startSymbol("{+");$interpolateProvider.endSymbol("+}");$routeProvider.when("/",{templateUrl:"/partials/campaign_list",controller:"CampaignListController",resolve:{login:loggedInPromise}});$routeProvider.when("/login",{templateUrl:"/partials/login",controller:"LoginController"});$routeProvider.when("/signup",{templateUrl:"/partials/signup",controller:"SignupController"});$routeProvider.when("/foo",{templateUrl:"/partials/login",controller:"FooController",resolve:{login:loggedInPromise}});$routeProvider.otherwise({redirectTo:"/"});});app.controller("MainController",function($scope,$route,$location,identity){return $scope.$on("$routeChangeError",function(event,d,u,reason){var destinationUrl;if(reason==="notLoggedIn"){destinationUrl=$location.url();$location.path("/login");return $location.search({destination:destinationUrl});}});});app.run(function($rootScope,$timeout,$q){return $rootScope.$waitOnce=function(timeout,events){var deferred,event,eventName,eventsMap,rejectCallback,removalFunctions,removeAll,resolve,resolveCallback,_i,_len;if(Object.isArray(events)){eventsMap={};for(_i=0,_len=events.length;_i<_len;_i++){event=events[_i];eventsMap[event]=true;}
events=eventsMap;}
deferred=$q.defer();removalFunctions=[];removeAll=function(){var removalFunction,_j,_len1,_results;_results=[];for(_j=0,_len1=removalFunctions.length;_j<_len1;_j++){removalFunction=removalFunctions[_j];_results.push(removalFunction());}
return _results;};if(timeout>0){$timeout(function(){removeAll();return deferred.reject({event:"timeout","arguments":[]});},timeout);}
resolveCallback=function(){var args,event;event=arguments[0],args=2<=arguments.length?__slice.call(arguments,1):[];removeAll();return deferred.resolve({event:event.name,"arguments":args});};rejectCallback=function(){var args,event;event=arguments[0],args=2<=arguments.length?__slice.call(arguments,1):[];removeAll();return deferred.reject({event:event.name,"arguments":args});};for(eventName in events){resolve=events[eventName];if(resolve){removalFunctions.push($rootScope.$on(eventName,resolveCallback));}else{removalFunctions.push($rootScope.$on(eventName,rejectCallback));}}
return deferred.promise;};});var module;module=angular.module("madacra.campaign",["madacra.socketio"]);module.factory("campaign",function($rootScope,socket){var CampaignService;CampaignService=(function(){CampaignService.name='CampaignService';function CampaignService(){var _this=this;this.campaigns={};socket.addEvents({"/campaign":["enumerate"]});$rootScope.$on("/campaign:enumerate",function(event,data){var campaign,campaigns,_i,_len,_results;campaigns=data.campaigns;_results=[];for(_i=0,_len=campaigns.length;_i<_len;_i++){campaign=campaigns[_i];_results.push(_this.campaigns[campaign._id]=campaign);}
return _results;});}
CampaignService.prototype.enumerate=function(){return socket.emit("/campaign","enumerate");};return CampaignService;})();return new CampaignService();});module.controller("CampaignListController",function($scope,campaign){campaign.enumerate();return $scope.getCampaigns=function(){return Object.values(campaign.campaigns);};});var module,__bind=function(fn,me){return function(){return fn.apply(me,arguments);};},__slice=[].slice,__indexOf=[].indexOf||function(item){for(var i=0,l=this.length;i<l;i++){if(i in this&&this[i]===item)return i;}return-1;};module=angular.module("madacra.socketio",[]);module.factory("socket",function($rootScope){var SocketService;SocketService=(function(){SocketService.name='SocketService';function SocketService(){this.emit=__bind(this.emit,this);this.addEvents=__bind(this.addEvents,this);this.addEvent=__bind(this.addEvent,this);this.socket=io.connect();this.events=[];}
SocketService.prototype.broadcastOnRootScope=function(eventName){return function(){var args;args=1<=arguments.length?__slice.call(arguments,0):[];return $rootScope.$apply(function(){return $rootScope.$broadcast.apply($rootScope,[eventName].concat(__slice.call(args)));});};};SocketService.prototype.getNamespace=function(namespace){if((namespace!=null)&&namespace!==""){return this.socket.of(namespace);}else{return this.socket;}};SocketService.prototype.addEvent=function(namespace,eventName){var name;name=""+namespace+":"+eventName;if(__indexOf.call(this.events,name)<0){return this.getNamespace(namespace).on(eventName,this.broadcastOnRootScope(name));}};SocketService.prototype.addEvents=function(eventMap){var eventName,eventNames,namespace,_results;_results=[];for(namespace in eventMap){eventNames=eventMap[namespace];_results.push((function(){var _i,_len,_results1;_results1=[];for(_i=0,_len=eventNames.length;_i<_len;_i++){eventName=eventNames[_i];_results1.push(this.addEvent(namespace,eventName));}
return _results1;}).call(this));}
return _results;};SocketService.prototype.emit=function(namespace,eventName,data){return this.getNamespace(namespace).emit(eventName,data);};return SocketService;})();return new SocketService();});var loggedInPromise,module,__bind=function(fn,me){return function(){return fn.apply(me,arguments);};};module=angular.module("madacra.identity",["madacra.socketio","controls.tooltip","controls.validators","ngCookies"]);loggedInPromise=function($q,identity){var result;result=$q.defer();if(identity.isAuthenticated()){result.resolve(true);}else{result.reject("notLoggedIn");}
return result.promise;};module.factory("identity",function($rootScope,$q,$timeout,$cookieStore,socket){var IdentityService;IdentityService=(function(){IdentityService.name='IdentityService';function IdentityService(){this.isAuthenticated=__bind(this.isAuthenticated,this);var _this=this;this.token=this.loadToken();this.username=null;socket.addEvents({"/identity":["changed","loginSuccessful","loginFailed","logoutSuccessful","signupSuccessful","signupFailed"]});$rootScope.$on("/identity:loginSuccessful",function(event,data){_this.token=data.token;_this.username=data.username;return _this.storeToken(_this.token);});$rootScope.$on("/identity:logoutSuccessful",function(event,data){_this.token=null;_this.username=null;return _this.removeToken();});if(this.token!=null){this.identify(this.token);}}
IdentityService.prototype.loadToken=function(){var _ref;return(_ref=$cookieStore.get("identityToken"))!=null?_ref:null;};IdentityService.prototype.storeToken=function(token){return $cookieStore.put("identityToken",token);};IdentityService.prototype.removeToken=function(){return $cookieStore.remove("identityToken");};IdentityService.prototype.identify=function(token){return socket.emit("/identity","identify",{token:token});};IdentityService.prototype.logIn=function(username,password){return socket.emit("/identity","login",{username:username,password:password});};IdentityService.prototype.logOut=function(){return socket.emit("/identity","logout");};IdentityService.prototype.isAuthenticated=function(){return this.token!=null;};IdentityService.prototype.signUp=function(username,password){return socket.emit("/identity","signup",{username:username,password:password});};return IdentityService;})();return new IdentityService();});module.controller("LoginController",function($scope,$rootScope,$route,$location,identity){$scope.loginUsername="";$scope.loginPassword="";$scope.loggingIn=false;$scope.serverError=null;return $scope.login=function(){var destination,p;$scope.loggingIn=true;destination=$location.search().destination||"/";identity.logIn($scope.loginUsername,$scope.loginPassword);p=$rootScope.$waitOnce(10000,{"/identity:loginSuccessful":true,"/identity:loginFailed":false});return p.then(function(){$scope.serverError=null;$scope.loggingIn=false;return $location.url(destination);},function(data){var _ref;switch(data.event){case"/identity:loginFailed":$scope.serverError=(_ref=data["arguments"])!=null?_ref[0]:void 0;break;default:$scope.serverError=data.event;}
return $scope.loggingIn=false;});};});module.controller("SignupController",function($scope,$rootScope,$location,identity){$scope.signupUsername="";$scope.signupPassword="";$scope.signupPasswordConfirmation="";$scope.signingUp=false;$scope.serverError=null;return $scope.signup=function(){var p;$scope.signingUp=true;identity.signUp($scope.signupUsername,$scope.signupPassword);p=$rootScope.$waitOnce(10000,{"/identity:loginSuccessful":true,"/identity:signupFailed":false});return p.then(function(){$scope.serverError=null;$scope.signingUp=false;return $location.url("/");},function(data){var _ref;switch(data.event){case"/identity:signupFailed":$scope.serverError=(_ref=data["arguments"])!=null?_ref[0]:void 0;break;default:$scope.serverError=data.event;}
return $scope.signingUp=false;});};});module.controller("IdentityIndicatorController",function($scope,$location,identity){$scope.getUsername=function(){return identity.username;};$scope.showIdentityPopup=function(value){return $scope.identityPopupVisiblity=value;};$scope.toggleIdentityPopup=function(){return $scope.showIdentityPopup(!$scope.identityPopupVisiblity);};return $scope.logOut=function(){identity.logOut();return $location.url("/login");};});var module;module=angular.module("controls.tooltip",[]);module.directive("tooltip",function(){return{link:function(scope,iElement,iAttrs){var animation,placement,selector,title,trigger,_ref,_ref1,_ref2;animation=(_ref=iAttrs.tooltipAnimation)!=null?_ref:true;placement=(_ref1=iAttrs.tooltipPlacement)!=null?_ref1:"top";selector=(_ref2=iAttrs.tooltipSelector)!=null?_ref2:false;title=iAttrs.tooltip;trigger=iAttrs.tooltipTrigger==="hover"?"hover":"manual";iElement.tooltip({animation:animation,placement:placement,selector:selector,title:title,trigger:trigger});iElement.tooltip("hide");if(trigger==="manual"){return scope.$watch(iAttrs.tooltipTrigger,function(value){if(value){return iElement.tooltip("show");}else{return iElement.tooltip("hide");}});}}};});var module;module=angular.module("controls.validators",[]);module.directive("equalTo",function(){return{require:"ngModel",link:function(scope,iElement,iAttrs,ctrl){var check;check=function(referenceValue,localValue){if(localValue!==referenceValue){return ctrl.$setValidity("equalTo",false);}else{return ctrl.$setValidity("equalTo",true);}};scope.$watch(iAttrs.equalTo,function(value){return check(value,scope[iAttrs.ngModel]);});ctrl.$parsers.unshift(function(viewValue){check(scope.$eval(iAttrs.equalTo),viewValue);return viewValue;});}};});module.directive("externalErrors",function(){return{require:"ngModel",link:function(scope,iElement,iAttrs,ctrl){scope.$watch(iAttrs.externalErrors,function(newValue,oldValue){var errorKey,errorValue,_results;_results=[];for(errorKey in newValue){errorValue=newValue[errorKey];_results.push(ctrl.$setValidity(errorKey,!errorValue));}
return _results;},true);}};});