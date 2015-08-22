/*global require:true, define:true, console:true, confirm:true, alert:true */

require.config({
    baseUrl: "/static/survey/js",
    //urlArgs: "bust=" + (new Date()).getTime(),
    paths: {
        "jquery": "../bower_components/jquery/dist/jquery.min",
        "bootstrap": "../bower_components/bootstrap/dist/js/bootstrap.min",
        "select2": "../bower_components/select2/select2.min",
        "jquery-cookie": "../bower_components/jquery-cookie/jquery.cookie"
    },
    shim: {
        "bootstrap": {
            deps: ["jquery"]
        },
        "select2": {
            deps: ["jquery"]
        },
        "jquery-cookie": {
            deps: ["jquery"]
        }
    },
    packages: []
});

require(["jquery", "bootstrap", "select2", "jquery-cookie"], function ($) {
    'use strict';

    // AJAX SETUP
    // --------------------------------------------------------------------------------------------------------------//
    var csrftoken = $.cookie('csrftoken');
    console.log(csrftoken);

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // BOOTSTRAP INIT
    // --------------------------------------------------------------------------------------------------------------//
    $('#organisation-description').popover({trigger: "hover"});
    $('[data-toggle="tooltip"]').tooltip();
    $('#id_countries.select2-field').select2({placeholder: "Start typing to select a country..."});
    $('#id_country_of_operation.select2-field').select2({placeholder: "Start typing to select a country..."});
    $('#id_currency.select2-field').select2({placeholder: "Start typing to select a currency..."});


    $('body').on('hidden.bs.modal', '.modal', function () {
        $(this).removeData('bs.modal');
    });

    $('#providerAddModal').on('loaded.bs.modal', function (e) {
        // do cool stuff here all day… no need to change bootstrap

        $('#provider_form').find('.select2-field').select2({placeholder: "Start typing to select a country..."});

        $('#other_service_provided_button').click(function (e) {
            e.preventDefault();
            var other = $('#other_service_provided')[0];
            var jsonForm = {'csrfmiddlewaretoken': csrftoken, 'name': other.value};
            //console.log('provider_form other_service_provided_button click event');
            //console.log(other.value);
            other.value = '';
            addServiceProvided(jsonForm);
            return false;
        });

        $('#other_reliable_button').click(function (e) {
            e.preventDefault();
            var other = $('#other_reliable')[0];
            var jsonForm = {'csrfmiddlewaretoken': csrftoken, 'name': other.value};
            //console.log('provider_form other_reliable_button click event');
            //console.log(other.value);
            other.value = '';
            addReliable(jsonForm);
            return false;
        });

        var checkedServicesIds = $('input[name=services_provided][checked=checked]').map(function () {
            return $(this).val();
        }).get();

        var strongServiceOptionIdsAll = $('input[name=strong_services]').map(function () {
            return $(this).val();
        }).get();

        console.log(checkedServicesIds);

        $.each(strongServiceOptionIdsAll, function (index, value) {
            //alert( index + ": " + value );
            if ($.inArray(value, checkedServicesIds) === -1) {
                $('#id_strong_services').find('input[value="' + value + '"]').parent().parent().remove();
            }
        });


        $('#id_services_provided').on('click', 'input:checkbox', function (e) {
            var checked = (e.currentTarget.checked) ? true : false;
            var optionId = e.currentTarget.value;
            var optionStr = $(e.currentTarget).parent().text();

            var field = 'strong_services';
            var addedOption = String.format(optionUncheckedTemplate, field, (parseInt(optionId) - 1), optionId, optionStr);

            if (checked) {
                $('#id_strong_services').append(addedOption);
            }
            else {
                $('#id_strong_services').find('input[value="' + optionId + '"]').parent().parent().remove();
            }

            console.log(addedOption);

        });
    });

    var challengesIds, challengesIdsAll;


    $("#update_biggest_challenge_1").click(function (event) {
        //event.preventDefault();
        challengesIds = $("div#id_challenges").find("input:checkbox:checked").map(function () {
            return this.value;
        }).toArray();
        var jsonForm = $('#challenge_form').serialize();
        console.log(jsonForm)
        saveChallenges(jsonForm);

    });
    $("#update_biggest_challenge_2").click(function (event) {
        //event.preventDefault();
        challengesIds = $("div#id_challenges").find("input:checkbox:checked").map(function () {
            return this.value;
        }).toArray();
        var jsonForm = $('#challenge_form').serialize();
        saveChallenges(jsonForm);
    });
    $("#update_biggest_challenge_3").click(function (event) {
        //event.preventDefault();
        challengesIds = $("div#id_challenges").find("input:checkbox:checked").map(function () {
            return this.value;
        }).toArray();
        var jsonForm = $('#challenge_form').serialize();
        saveChallenges(jsonForm);
    });


    $('#challengeDetailModal').on('loaded.bs.modal', function (e) {
        //challengesIds = $('input[name=challenges][checked=checked]').map(function () {
        //    return $(this).val();
        //}).get();

        challengesIdsAll = $('select#id_challenge').find('option').map(function () {
            return $(this).val();
        }).get();


        console.log(challengesIds);
        console.log(challengesIdsAll);


        $.each(challengesIdsAll, function (index, value) {
            //alert( index + ": " + value );
            if ($.inArray(value, challengesIds) === -1) {
                $('select#id_challenge').find('option[value="' + value + '"]').remove();
            }
        });

        $('#other_attempted_services_button').on('click', function (e) {
            e.preventDefault();

            var other = $('#other_attempted_services')[0];
            var jsonForm = {'csrfmiddlewaretoken': csrftoken, 'name': other.value};

            console.log(other.value);
            other.value = '';

            addAttemptedServices(jsonForm);
            return false;
        });


    });

    $('#id_revenue_streams').on('change', 'input', function (e) {
        var maxAllowed = 3;
        var cnt = $("input[name='revenue_streams']:checked").length;
        if (cnt > maxAllowed) {
            $(this).prop("checked", "");
            alert('You can select maximum ' + maxAllowed + ' revenue streams.');
        }
    });

    var optionUncheckedTemplate = hereDoc(function () {/*!
     <div class="checkbox">
     <label for="id_{0}_{1}">
     <input class="" id="id_{0}_{1}" name="{0}" title="" value="{2}" type="checkbox">{3}
     </label>
     </div>
     */
    });


    // DEEP LINKING
    // --------------------------------------------------------------------------------------------------------------//
    $(document).ready(function () {

        // queryStrip
        function queryStrip(string) {
            string = string.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
            var regex = new RegExp('[\\?&]' + string + '=([^&#]*)'),
                results = regex.exec(location.search);
            return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ''));
        }

        // Show bootstrap modal on load
        // If the modal id="terms", you can show it on page load by appending `?modal=terms` to the URL
        var modalString = queryStrip('modal'),
            modalToShow = '#' + modalString;
        if (modalString !== '') {
            $(modalToShow).modal('show');
        }

        // Show bootstrap tooltip on load
        // If the tooltip id="artistName", you can show it on page load by appending `?tooltip=artistName to the URL
        var tooltipString = queryStrip('tooltip'),
            tooltipToShow = '#' + tooltipString;
        if (tooltipString !== '') {
            $(tooltipToShow).tooltip('show');
        }

        // Show bootstrap popover on load
        // If the popover id="moreInfo", you can show it on page load by appending `?popover=moreInfo` to the URL
        var popoverString = queryStrip('popover'),
            popoverToShow = '#' + popoverString;
        if (popoverString !== '') {
            $(popoverToShow).popover('show');
        }

        // Show bootstrap tab on load
        // If the tab id="friendRequests", you can show it on page load by appending `?tab=friendRequests` to the URL
        var tabString = queryStrip('tab');
        if (tabString !== '') {
            $('.nav-tabs a[href=#' + tabString + ']').tab('show');
        }
    });


    //Non prototype modifying
    if (!String.format) {
        String.format = function (format) {
            var args = Array.prototype.slice.call(arguments, 1);
            return format.replace(/{(\d+)}/g, function (match, number) {
                return typeof args[number] !== 'undefined' ? args[number] : match;
            });
        };
    }

    function hereDoc(f) {
        return f.toString().
            replace(/^[^\/]+\/\*!?/, '').
            replace(/\*\/[^\/]+$/, '');
    }


    // AJAX FORM SUBMISSION
    // --------------------------------------------------------------------------------------------------------------//

    // Delete post on click
    $("#provider").on('click', 'a[id^=delete-provider-]', function () {
        var providerPk = $(this).attr('id').split('-')[2];
        console.log(providerPk); // sanity check
        deleteProvider(providerPk);
    });

    function deleteProvider(providerPk) {
        if (confirm('are you sure you want to remove this post?') === true) {
            $.ajax({
                url: "/provider/" + providerPk + "/delete/", // the endpoint
                type: "DELETE", // http method
                data: {pk: providerPk}, // data sent with the delete request
                success: function () {
                    // hide the post
                    $('#provider-' + providerPk).hide(); // hide the post on success
                    console.log("Provider deletion successful");
                },

                error: function (xhr) {
                    // Show an error
                    $('#results').html("<div class='alert-box alert radius' data-alert> Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>");
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
        } else {
            return false;
        }
    }


    // AJAX OTHER OPTIONS
    // --------------------------------------------------------------------------------------------------------------//
    $('#other_challenge_button').on('click', function (e) {
        e.preventDefault();

        var other = $('#other_challenge')[0];
        var jsonForm = {'csrfmiddlewaretoken': csrftoken, 'name': other.value};

        console.log(other.value);
        other.value = '';

        addChallenge(jsonForm);
        return false;
    });


    $('#other_revenue_stream_button').on('click', function (e) {
        e.preventDefault();

        var other = $('#other_revenue_stream')[0];
        var jsonForm = {'csrfmiddlewaretoken': csrftoken, 'name': other.value};

        console.log(other.value);
        other.value = '';

        addRevenueStream(jsonForm);
        return false;
    });

    $('#other_roi_period_button').on('click', function (e) {
        e.preventDefault();

        var other = $('#other_roi_period')[0];
        var jsonForm = {'csrfmiddlewaretoken': csrftoken, 'name': other.value};

        console.log(other.value);
        other.value = '';

        addPeriod(jsonForm);
        return false;
    });

    function saveChallenges(jsonForm) {
        $.ajax({
            url: "/challenge/",
            type: "POST",
            traditional: true,
            data: jsonForm,

            success: function (json) {
                var message = 'Success';
                console.log(message);

            },
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }

    var optionTemplate = hereDoc(function () {/*!
     <div class="checkbox">
     <label for="id_{0}_{1}">
     <input class="" id="id_{0}_{1}" name="{0}" title="" value="{2}" type="checkbox">{3}
     </label>
     </div>
     */
    });

    function addServiceProvided(jsonForm) {
        $.ajax({
            url: "/service/add/",
            type: "POST",
            traditional: true,
            data: jsonForm,

            success: function (json) {
                var field = 'services_provided';
                var addedOption = String.format(optionTemplate, field, (parseInt(json.id) - 1), json.id, json.name);
                console.log(addedOption);
                $("#id_" + field).append(addedOption);
            },
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }

    function addReliable(jsonForm) {
        $.ajax({
            url: "/reliable/add/",
            type: "POST",
            traditional: true,
            data: jsonForm,

            success: function (json) {
                var field = 'trust_attributes';
                var addedOption = String.format(optionTemplate, field, (parseInt(json.id) - 1), json.id, json.name);
                console.log(addedOption);
                $("#id_" + field).append(addedOption);
            },
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    }

    function addRevenueStream(jsonForm) {
        $.ajax({
            url: "/service/add/",
            type: "POST",
            traditional: true,
            data: jsonForm,

            success: function (json) {
                var field = 'revenue_stream';
                var addedOption = '<option value=' + parseInt(json.id) + '>' + json.name + '</option>';
                //var addedOption = String.format(optionTemplate, field, (parseInt(json.id) - 1), json.id, json.name);
                console.log(addedOption);
                //$("#id_" + field).append(addedOption);
                $("select#id_" + field + '_1').append(addedOption);
                $("select#id_" + field + '_2').append(addedOption);
                $("select#id_" + field + '_3').append(addedOption);
                //$('#id_revenue_stream_1').append('<option value=46>Hello World</option>')
            },
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });

    }

    function addPeriod(jsonForm) {
        $.ajax({
            url: "/period/add/",
            type: "POST",
            traditional: true,
            data: jsonForm,

            success: function (json) {
                var field = 'acceptable_roi_wait';
                var addedOption = '<option value=' + parseInt(json.id) + '>' + json.name + '</option>';
                //var addedOption = String.format(optionTemplate, field, (parseInt(json.id) - 1), json.id, json.name);
                console.log(addedOption);
                //$("#id_" + field).append(addedOption);
                $("select#id_" + field).append(addedOption);
                //$('#id_revenue_stream_1').append('<option value=46>Hello World</option>')
            },
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });

    }


    function addChallenge(jsonForm) {
        $.ajax({
            url: "/challenge/add/",
            type: "POST",
            traditional: true,
            data: jsonForm,

            success: function (json) {
                var field = 'challenges';
                var addedOption = String.format(optionTemplate, field, (parseInt(json.id) - 1), json.id, json.name);
                console.log(addedOption);
                $("#id_" + field).append(addedOption);
            },
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });

    }

    function addAttemptedServices(jsonForm) {
        $.ajax({
            url: "/service/add/",
            type: "POST",
            traditional: true,
            data: jsonForm,

            success: function (json) {
                var field = 'attempted_services';
                var addedOption = String.format(optionTemplate, field, (parseInt(json.id) - 1), json.id, json.name);
                console.log(addedOption);
                $("#id_" + field).append(addedOption);
            },
            error: function (xhr) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });

    }
});