/**
 * Created by dimitris on 4/9/2017.
 */
(function($) {

    // Initialize Firebase
    var firebaseConfig = {
        apiKey: FirebaseSettings.apiKey,
        authDomain: FirebaseSettings.authDomain,
        databaseURL: FirebaseSettings.databaseURL,
        projectId: FirebaseSettings.projectId,
        messagingSenderId: FirebaseSettings.messagingSenderId
    };
    firebase.initializeApp(firebaseConfig);

    FirebaseListener = function(params) {
        var config = $.extend({
            resourceUrl: '/',
            callback: function(value) {}
        }, params);

        var ref = firebase.database().ref(config.resourceUrl);
        ref.on('value', function(snapshot) {
            if (snapshot.val() !== null) {
                config.callback(snapshot.val());
            }
        });

        return this;
    };
})(django.jQuery);
