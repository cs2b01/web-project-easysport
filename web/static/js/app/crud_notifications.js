$(function(){
    var url = "http://18.228.148.139/notifications";
    var lookupData = [
    { id: "OK", show: "OK" },
    { id: "WARNING", show: "WARNING" },];

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
            dataField: "date",
            dataType: "datetime",
            allowEditing: false
        }, {
            dataField: "text"
        }, {
            dataField: "type",
            lookup: {
                  dataSource: lookupData,
                  valueExpr: 'id',
                  displayExpr: 'show'
                }
        } ]
    }).dxDataGrid("instance");
});
