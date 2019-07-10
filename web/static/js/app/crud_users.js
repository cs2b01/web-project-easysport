$(function(){
    var url = "http://18.228.148.139/users";
    var lookupData = [
    { id: true, show: "Administrador" },
    { id: false, show: "Usuario" }];

    $("#grid").dxDataGrid({
        dataSource: DevExpress.data.AspNet.createStore({
            key: "id",
            loadUrl: url ,
            insertUrl: url ,
            updateUrl: url ,
            deleteUrl: url ,
            onBeforeSend: function(method, ajaxOptions) {
                ajaxOptions.xhrFields = { withCredentials: true };
            }
        }),
        editing: {
            allowUpdating: true,
            allowDeleting: true,
            allowAdding: true
        },
        remoteOperations: {
            sorting: true,
            paging: true
        },
        paging: {
            pageSize: 12
        },
        pager: {
            showPageSizeSelector: true,
            allowedPageSizes: [8, 12, 20]
        },
        columns: [{
            dataField: "id",
            dataType: "number",
            allowEditing: false
        }, {
            dataField: "firstName"
        }, {
            dataField: "lastName"
        }, {
            dataField: "isAdmin",
            lookup: {
                  dataSource: lookupData,
                  valueExpr: 'id',
                  displayExpr: 'show'
                }
        }, {
            dataField: "email"
        }, {
            dataField: "password",
            dataType: "Password"
        } ]
    }).dxDataGrid("instance");
});
