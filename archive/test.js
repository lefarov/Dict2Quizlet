$.get(
    "https://dict.leo.org/ende/",
    {
        "search" : "Welt"
    },
    function(data) {
       alert("page content: " + data);
    }
);