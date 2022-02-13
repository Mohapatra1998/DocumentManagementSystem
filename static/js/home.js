$( function() {
    var availableTags = [
        {% for d in document %}
            "{{d.name}}",
        {% endfor %}
    ];
    $( "#tags" ).autocomplete({
      source: availableTags
    });
  } );