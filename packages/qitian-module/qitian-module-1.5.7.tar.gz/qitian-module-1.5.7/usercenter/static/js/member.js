var UIGeneral = function () {
    var a = function () {
        jQuery().pulsate && 1 != App.isIE8() && jQuery().pulsate && (jQuery("#pulsate-regular").pulsate({color: "#bf1c56"}), jQuery("#pulsate-once").click(function () {
            $("#pulsate-once-target").pulsate({color: "#399bc3", repeat: !1})
        }), jQuery("#pulsate-crazy").click(function () {
            $("#pulsate-crazy-target").pulsate({color: "#fdbe41", reach: 50, repeat: 10, speed: 100, glow: !0})
        }))
    }, e = function () {
        $("#dynamic_pager_demo1").bootpag({
            paginationClass: "pagination",
            next: '<i class="fa fa-angle-right"></i>',
            prev: '<i class="fa fa-angle-left"></i>',
            total: 6,
            page: 1
        }).on("page", function (a, e) {
            $("#dynamic_pager_content1").html("Page " + e + " content here")
        }), $("#dynamic_pager_demo2").bootpag({
            paginationClass: "pagination pagination-sm",
            next: '<i class="fa fa-angle-right"></i>',
            prev: '<i class="fa fa-angle-left"></i>',
            total: 24,
            page: 1,
            maxVisible: 6
        }).on("page", function (a, e) {
            $("#dynamic_pager_content2").html("Page " + e + " content here")
        })
    };
    return {
        init: function () {
            a(), e()
        }
    }
}();
jQuery(document).ready(function () {
    UIGeneral.init()
});