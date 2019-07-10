$(function(){
    var url = "http://18.228.148.139/championship";
    var lookupData = [
    { id: "sailing", show: "sailing" },
    { id: "soccer", show: "soccer" }];

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
            dataField: "title"
        }, {
            dataField: "description"
        },{
            dataField: "category",
            lookup: {
                  dataSource: lookupData,
                  valueExpr: 'id',
                  displayExpr: 'show'
                }
        }, {
            dataField: "price",
            dataType: "number"
        },{
            dataField: "startDate"
        }, {
            dataField: "endDate"
        }, {
            dataField: "maxCompetitors"
        }, {
            dataField: "location"
        } ]
    }).dxDataGrid("instance");
});
