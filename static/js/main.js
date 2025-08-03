document.addEventListener("DOMContentLoaded", () => {
  // 1. VALIDACIÓN GENERAL DE FORMULARIOS

  const forms = document.querySelectorAll("form");

  forms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      const inputs = form.querySelectorAll("input, select");
      let valid = true;

      inputs.forEach((input) => {
        if (input.value.trim() === "") {
          input.style.borderColor = "red";
          valid = false;
        } else {
          input.style.borderColor = "#ccc";
        }
      });

      if (!valid) {
        e.preventDefault();
        alert("Por favor completa todos los campos.");
        return;
      }

      if (!confirm("¿Confirmas enviar el formulario?")) {
        e.preventDefault();
      }
    });
  });

  // 2. VALIDACIÓN ESPECÍFICA DE PRODUCTO FORM
  
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", (e) => {
      let valid = true;

      const nombre = document.querySelector("#id_nombre");
      const sku = document.querySelector("#id_sku");
      const stockActual = document.querySelector("#id_stock_actual");
      const stockMinimo = document.querySelector("#id_stock_minimo");

      if (nombre && !nombre.value.trim()) {
        alert("El nombre del producto es obligatorio.");
        valid = false;
      }

      if (sku && !sku.value.trim()) {
        alert("El SKU es obligatorio.");
        valid = false;
      }

      if (stockActual && (Number(stockActual.value) < 0 || isNaN(stockActual.value))) {
        alert("Stock actual debe ser un número positivo.");
        valid = false;
      }

      if (stockMinimo && (Number(stockMinimo.value) < 0 || isNaN(stockMinimo.value))) {
        alert("Stock mínimo debe ser un número positivo.");
        valid = false;
      }

      // 3. VALIDACIÓN DE FECHAS EN RESUMEN DE VENTAS
      
      const fechaInicio = document.querySelector("#id_fecha_inicio");
      const fechaFin = document.querySelector("#id_fecha_fin");

      if (fechaInicio && fechaFin) {
        const inicio = new Date(fechaInicio.value);
        const fin = new Date(fechaFin.value);
        if (inicio > fin) {
          alert("La fecha de inicio no puede ser mayor a la fecha de fin.");
          valid = false;
        }
      }

     // 4. VALIDACIÓN DE CATEGORÍA EN REPORTES
      
      const categoria = document.querySelector("#id_categoria");
      if (categoria && categoria.value === "") {
        alert("Por favor selecciona una categoría.");
        valid = false;
      }

      if (!valid) e.preventDefault();
    });
  }

  // 5. CONFIRMACIÓN AL ELIMINAR PRODUCTO
  
  const botonesEliminar = document.querySelectorAll(".btn-eliminar");

  botonesEliminar.forEach((boton) => {
    boton.addEventListener("click", (event) => {
      const confirmado = confirm("¿Estás seguro que quieres eliminar este producto?");
      if (!confirmado) {
        event.preventDefault();
      }
    });
  });
});




