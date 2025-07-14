var counter = 0;
document.addEventListener('DOMContentLoaded', function() {
    let select = this.getElementById("id_workflowscript_set-0-script")

    select.addEventListener('change', function() {
        console.log("Script select changed:", this.value);
        let dataScript = select.getElementsByClassName('script-info-container');
        console.log("Data script:", dataScript);
    });
})