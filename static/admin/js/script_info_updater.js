var counter = 0;
document.addEventListener('DOMContentLoaded', function() {
    let select = this.getElementById("id_workflowscript_set-0-script");

    select.addEventListener('change', function() {
        console.log("Script select changed:", this.value);
        let scriptId = this.value;
        let url = `/api/scripts/${scriptId}`;
        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                console.log("Datos del script:", data);
                // Mostrar información detallada del script
                let display = document.querySelector('.field-script_info_display');
                if (display) {
                    // Crear contenido HTML con más información
                    let contentPreview = data.content 
                        ? (data.content.length > 100 
                            ? data.content.substring(0, 100) + '...' 
                            : data.content)
                        : 'Sin contenido';
                    
                    let createdDate = data.created_at 
                        ? new Date(data.created_at).toLocaleDateString('es-ES')
                        : 'N/A';
                    
                    let updatedDate = data.updated_at 
                        ? new Date(data.updated_at).toLocaleDateString('es-ES')
                        : 'N/A';
                    
                    let statusIcon = data.is_active ? '✅' : '❌';
                    let statusText = data.is_active ? 'Activo' : 'Inactivo';
                    
                    display.innerHTML = `
                        <div style="border: 1px solid #ddd; padding: 10px; border-radius: 4px; background-color: #f9f9f9;">
                            <h4 style="margin: 0 0 8px 0; color: #333;">📄 ${data.name || 'Sin nombre'}</h4>
                            <div style="margin-bottom: 6px;">
                                <strong>Estado:</strong> ${statusIcon} ${statusText} | 
                                <strong>Orden:</strong> ${data.order || 0}
                            </div>
                            <div style="margin-bottom: 6px;">
                                <strong>Creado:</strong> ${createdDate} | 
                                <strong>Actualizado:</strong> ${updatedDate}
                            </div>
                            <div style="margin-bottom: 8px;">
                                <strong>Código (preview):</strong>
                            </div>
                            <pre style="background-color: #f4f4f4; padding: 8px; border-radius: 3px; font-size: 12px; max-height: 80px; overflow-y: auto; margin: 0;">${contentPreview}</pre>
                        </div>
                    `;
                }
            })
            .catch(error => {
                console.error("Error al obtener datos del script:", error);
                let display = document.querySelector('.field-script_info_display');
                if (display) {
                    display.innerHTML = `
                        <div style="border: 1px solid #e74c3c; padding: 10px; border-radius: 4px; background-color: #fdf2f2; color: #e74c3c;">
                            ❌ Error al cargar información del script
                        </div>
                    `;
                }
            });
    });
});