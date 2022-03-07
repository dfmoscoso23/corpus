{% block js %}
    <script language="javascript">
        //alert('funcionou');
        $('#id_zonas_form').change(function() {populateSubZonas(this)});
        // $('#id_description').addClass('descriptions');

        subzonas = {{ formulario_zonas.sub | safe }}
        zonas = {{ formulario_zonas.lista_zonas | safe}};
        populateZonas();
        $("#id_subzonas_form").empty();
        $("#id_subzonas_form").append('<option value="" disabled selected>Primero selecciona una zona</option>');


        function populateZonas() {
            $('#id_zonas_form').empty();
            $("#id_zonas_form").append('<option value="" disabled selected>Select your option</option>');
            $.each(zonas, function(v) {
                $('#id_zonas_form')
                    .append($("<option></option>")
                    .attr("value", zonas[v])
                    .text(zonas[v]));
            });
        }

        function populateSubZonas(event) {
            zona = $("#id_zonas_form option:selected").text();
            $("#id_subzonas_form").empty();
            $("#id_subzonas_form").append('<option value="" disabled selected>Select your option</option>');
            for (let [b, dic_zona] of Object.entries(subzonas)) {
                if (b == zona) {
                    //alert(b);
                    for (subzo in dic_zona) {
                        $('#id_subzonas_form')
                            .append($("<option></option>")
                                .attr("value", dic_zona[subzo])
                                .text(dic_zona[subzo]));
                    }
                }
            }
        }
    </script>
{% endblock %}