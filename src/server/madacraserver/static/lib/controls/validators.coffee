module = angular.module "controls.validators", []

module.directive "equalTo", ->
    return {
        require: "ngModel"
        link: (scope, iElement, iAttrs, ctrl) ->
            check = (referenceValue, localValue) ->
                if localValue != referenceValue
                    ctrl.$setValidity("equalTo", false)
                else
                    ctrl.$setValidity("equalTo", true)

            scope.$watch iAttrs.equalTo, (value) ->
                check(value, scope[iAttrs.ngModel])

            ctrl.$parsers.unshift (viewValue) ->
                check(scope.$eval(iAttrs.equalTo), viewValue)
                return viewValue

            return
    }

module.directive "externalErrors", ->
    return {
        require: "ngModel"
        link: (scope, iElement, iAttrs, ctrl) ->
            scope.$watch iAttrs.externalErrors, (newValue, oldValue) ->
                for errorKey, errorValue of newValue
                    ctrl.$setValidity(errorKey, not errorValue)
            , true
            return
    }
