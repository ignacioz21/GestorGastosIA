/**
 * Dashboard.js - Gráficas de gastos por categoría
 * Maneja la creación y actualización de gráficas Chart.js
 */

// Variables globales
let expenseChart = null;
let dashboardConfig = {
    apiUrl: '/api/gastos-categoria',
    chartColors: [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
        '#9966FF', '#FF9F40', '#FF6B9D', '#C9CBCF',
        '#4ECDC4', '#45B7D1'
    ],
    animationDuration: 1500,
    updateInterval: null // Para auto-actualización
};

/**
 * Inicializar el dashboard cuando el DOM esté listo
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inicializando Dashboard de Gastos...');
    
    // Verificar que Chart.js esté cargado
    if (typeof Chart === 'undefined') {
        console.error('❌ Chart.js no está cargado. Asegúrate de incluirlo antes que dashboard.js');
        mostrarError('Chart.js no está disponible');
        return;
    }
    
    // Verificar que el canvas exista
    const canvas = document.getElementById('expenseChart');
    if (!canvas) {
        console.warn('⚠️ Canvas #expenseChart no encontrado. La gráfica no se creará.');
        return;
    }
    
    // Cargar datos iniciales
    cargarGraficos();
    
    // Auto-actualizar cada 5 minutos (opcional)
    // configurarAutoActualizacion(300000); // 5 minutos = 300000ms
});

/**
 * Cargar datos del servidor y crear/actualizar la gráfica
 */
async function cargarGraficos() {
    try {
        mostrarCargando(true);
        ocultarError();
        
        console.log('📡 Solicitando datos desde:', dashboardConfig.apiUrl);
        
        const response = await fetch(dashboardConfig.apiUrl);
        
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
        }
        
        const datos = await response.json();
        console.log('📊 Datos recibidos:', datos);
        
        if (datos.success) {
            // Normalizar nombres de propiedades
            const datosNormalizados = {
                categorias: datos.categorias || datos.categories || [],
                montos: datos.montos || datos.amounts || [],
                total_gastos: datos.total_gastos || datos.total || 0,
                success: true
            };
            
            console.log('📊 Datos normalizados:', datosNormalizados);
            
            if (datosNormalizados.categorias && datosNormalizados.categorias.length > 0) {
                crearGraficaBarras(datosNormalizados);
                mostrarEstadisticas(datosNormalizados);
                console.log('✅ Gráfica y estadísticas actualizadas correctamente');
            } else {
                console.warn('⚠️ No hay datos disponibles');
                mostrarMensaje('📋 No hay datos de gastos disponibles');
            }
        } else {
            throw new Error(datos.error || 'Error desconocido del servidor');
        }
        
    } catch (error) {
        console.error('❌ Error al cargar datos:', error);
        mostrarError(`Error al cargar datos: ${error.message}`);
        
        // Cargar datos de ejemplo como fallback
        console.log('🔄 Cargando datos de ejemplo como respaldo...');
        cargarDatosEjemplo();
        
    } finally {
        mostrarCargando(false);
    }
}

/**
 * Alias para mantener compatibilidad
 */
function cargarGraficaGastos() {
    return cargarGraficos();
}

/**
 * Crear la gráfica de barras horizontales con Chart.js
 */
function crearGraficaBarras(datos) {
    const canvas = document.getElementById('expenseChart');
    if (!canvas) {
        console.error('❌ Canvas no encontrado');
        return;
    }
    
    const ctx = canvas.getContext('2d');
    
    // Destruir gráfica anterior si existe
    if (expenseChart) {
        expenseChart.destroy();
    }
    
    // Configuración de la gráfica
    const config = {
        type: 'bar',
        data: {
            labels: datos.categorias,
            datasets: [{
                label: 'Gastos ($)',
                data: datos.montos,
                backgroundColor: dashboardConfig.chartColors.slice(0, datos.categorias.length),
                borderColor: dashboardConfig.chartColors.slice(0, datos.categorias.length),
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false,
                hoverBackgroundColor: dashboardConfig.chartColors.slice(0, datos.categorias.length).map(color => color + 'CC'),
                hoverBorderWidth: 3
            }]
        },
        options: {
            indexAxis: 'y', // Barras horizontales
            responsive: true,
            maintainAspectRatio: false,
            
            plugins: {
                legend: { 
                    display: false 
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleColor: 'white',
                    bodyColor: 'white',
                    borderColor: '#666',
                    borderWidth: 1,
                    callbacks: {
                        title: function(context) {
                            return `📂 ${context[0].label}`;
                        },
                        label: function(context) {
                            const valor = context.parsed.x;
                            const porcentaje = datos.total_gastos > 0 ? 
                                ((valor / datos.total_gastos) * 100).toFixed(1) : 0;
                            return [
                                `💰 $${valor.toFixed(2)}`,
                                `📊 ${porcentaje}% del total`
                            ];
                        }
                    }
                }
            },
            
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(0);
                        },
                        color: '#666'
                    },
                    grid: {
                        color: 'rgba(0,0,0,0.1)'
                    },
                    title: {
                        display: true,
                        text: 'Monto Gastado ($)',
                        color: '#333',
                        font: {
                            weight: 'bold',
                            size: 12
                        }
                    }
                },
                y: {
                    ticks: {
                        color: '#666',
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Categorías',
                        color: '#333',
                        font: {
                            weight: 'bold',
                            size: 12
                        }
                    }
                }
            },
            
            animation: {
                duration: dashboardConfig.animationDuration,
                easing: 'easeInOutQuart'
            },
            
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    };
    
    // Crear la gráfica
    expenseChart = new Chart(ctx, config);
    
    console.log('✅ Gráfica creada exitosamente');
}

/**
 * Mostrar estadísticas adicionales
 */
function mostrarEstadisticas(datos) {
    console.log('📈 Actualizando estadísticas con:', datos);
    
    const container = document.getElementById('statsContainer');
    if (!container) {
        console.warn('⚠️ Container #statsContainer no encontrado');
        return;
    }
    
    // Verificar que tengamos datos válidos
    if (!datos.categorias || !datos.montos || datos.categorias.length === 0) {
        container.innerHTML = '<div class="stat-item"><span class="stat-label">⚠️ No hay datos para mostrar</span></div>';
        return;
    }
    
    const total = datos.total_gastos || 0;
    const promedio = datos.categorias.length > 0 ? total / datos.categorias.length : 0;
    const categoriaMayor = datos.categorias[0] || 'N/A';
    const gastoMayor = datos.montos[0] || 0;
    const categoriaMenor = datos.categorias[datos.categorias.length - 1] || 'N/A';
    const gastoMenor = datos.montos[datos.montos.length - 1] || 0;
    
    console.log(`📊 Estadísticas calculadas - Total: ${total}, Promedio: ${promedio.toFixed(2)}, Mayor: ${categoriaMayor} (${gastoMayor})`);
    
    const statsHtml = `
        <div class="stat-item">
            <span class="stat-label">💵 Total Gastado</span>
            <span class="stat-value">${total.toFixed(2)}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">📊 Promedio por Categoría</span>
            <span class="stat-value">${promedio.toFixed(2)}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">🥇 Categoría Principal</span>
            <span class="stat-value">${categoriaMayor}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">🔥 Mayor Gasto</span>
            <span class="stat-value">${gastoMayor.toFixed(2)}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">💚 Categoría Menor</span>
            <span class="stat-value">${categoriaMenor}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">📈 Total de Categorías</span>
            <span class="stat-value">${datos.categorias.length}</span>
        </div>
    `;
    
    // Actualizar el contenido
    container.innerHTML = statsHtml;
    
    // Agregar una pequeña animación de entrada
    container.style.opacity = '0';
    setTimeout(() => {
        container.style.transition = 'opacity 0.3s ease-in-out';
        container.style.opacity = '1';
    }, 100);
    
    console.log('✅ Estadísticas actualizadas correctamente');
}

/**
 * Mostrar/ocultar indicador de carga
 */
function mostrarCargando(mostrar) {
    console.log(`🔄 ${mostrar ? 'Mostrando' : 'Ocultando'} indicador de carga`);
    
    const loading = document.getElementById('chartLoading');
    if (loading) {
        loading.style.display = mostrar ? 'flex' : 'none';
    }
    
    // También manejar el loading de estadísticas si existe
    const statsContainer = document.getElementById('statsContainer');
    if (statsContainer && mostrar) {
        statsContainer.innerHTML = '<div class="stats-loading">Cargando estadísticas</div>';
    }
}

/**
 * Ocultar mensaje de error
 */
function ocultarError() {
    const errorContainer = document.getElementById('chartError');
    if (errorContainer) {
        errorContainer.style.display = 'none';
    }
}

/**
 * Mostrar mensaje de error
 */
function mostrarError(mensaje) {
    const container = document.getElementById('chartError') || crearContainerError();
    container.innerHTML = `
        <div class="error-message">
            ⚠️ ${mensaje}
            <button class="refresh-btn" onclick="cargarGraficos()">🔄 Reintentar</button>
        </div>
    `;
    container.style.display = 'block';
}

/**
 * Mostrar mensaje informativo en el canvas
 */
function mostrarMensaje(mensaje) {
    const canvas = document.getElementById('expenseChart');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        
        // Limpiar canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Configurar texto
        ctx.fillStyle = '#666';
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        
        // Obtener dimensiones reales del canvas
        const rect = canvas.getBoundingClientRect();
        const x = canvas.width / 2;
        const y = canvas.height / 2;
        
        ctx.fillText(mensaje, x, y);
        
        console.log('💬 Mensaje mostrado en canvas:', mensaje);
    }
}

/**
 * Crear contenedor de error si no existe
 */
function crearContainerError() {
    const container = document.createElement('div');
    container.id = 'chartError';
    container.className = 'error-container';
    container.style.cssText = `
        display: none;
        background: #fee2e2;
        color: #dc2626;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        text-align: center;
    `;
    
    const chartContainer = document.getElementById('expenseChart')?.parentNode;
    if (chartContainer) {
        chartContainer.appendChild(container);
    }
    
    return container;
}

/**
 * Cargar datos de ejemplo como fallback
 */
function cargarDatosEjemplo() {
    console.log('📋 Cargando datos de ejemplo...');
    
    const datosEjemplo = {
        success: true,
        categorias: ['Alimentación', 'Transporte', 'Entretenimiento', 'Salud', 'Servicios'],
        montos: [1250.75, 890.30, 650.50, 420.00, 380.25],
        total_gastos: 3591.80
    };
    
    crearGraficaBarras(datosEjemplo);
    mostrarEstadisticas(datosEjemplo);
    
    // Mostrar advertencia en la consola
    console.warn('⚠️ Mostrando datos de ejemplo - datos reales no disponibles');
}

/**
 * Actualizar la gráfica (función pública para llamar desde otros scripts)
 */
function actualizarGrafica() {
    console.log('🔄 Actualizando gráfica...');
    return cargarGraficos();
}

/**
 * Configurar auto-actualización
 */
function configurarAutoActualizacion(intervalo) {
    if (dashboardConfig.updateInterval) {
        clearInterval(dashboardConfig.updateInterval);
    }
    
    dashboardConfig.updateInterval = setInterval(() => {
        console.log('🔄 Auto-actualizando gráfica...');
        cargarGraficos();
    }, intervalo);
    
    console.log(`⏰ Auto-actualización configurada cada ${intervalo/1000} segundos`);
}

/**
 * Detener auto-actualización
 */
function detenerAutoActualizacion() {
    if (dashboardConfig.updateInterval) {
        clearInterval(dashboardConfig.updateInterval);
        dashboardConfig.updateInterval = null;
        console.log('⏹️ Auto-actualización detenida');
    }
}

/**
 * Configurar la URL de la API (útil para diferentes entornos)
 */
function configurarAPI(url) {
    dashboardConfig.apiUrl = url;
    console.log('🔗 URL de API configurada:', url);
}

/**
 * Limpiar recursos al salir de la página
 */
window.addEventListener('beforeunload', function() {
    detenerAutoActualizacion();
    if (expenseChart) {
        expenseChart.destroy();
    }
});

// Exponer funciones globalmente para uso en otros scripts
window.DashboardGastos = {
    actualizar: actualizarGrafica,
    cargar: cargarGraficos,
    configurarAPI: configurarAPI,
    configurarAutoActualizacion: configurarAutoActualizacion,
    detenerAutoActualizacion: detenerAutoActualizacion,
    mostrarDatosEjemplo: cargarDatosEjemplo
};