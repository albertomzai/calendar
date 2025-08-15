describe('Calendario Interactivo - Pruebas E2E', () => {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const day = String(today.getDate()).padStart(2, '0');
  const dateStr = `${year}-${month}-${day}`;

  it('debe crear, mover y eliminar un evento', () => {
    // Visitar la aplicación
    cy.visit('/');

    // Verificar que el calendario se muestra
    cy.get('[data-testid="calendar"]').should('exist');

    // Seleccionar un día (hoy)
    cy.get(`[data-testid="day-${dateStr}"]`).click();

    // Completar formulario de evento
    const eventTitle = 'Prueba Cypress';
    cy.get('[data-testid="input-title"]').type(eventTitle);
    cy.get('[data-testid="input-start-date"]').clear().type(dateStr);
    cy.get('[data-testid="input-end-date"]').clear().type(dateStr);
    cy.get('[data-testid="btn-save-event"]').click();

    // Verificar que el evento aparece en el calendario
    cy.contains(eventTitle).should('be.visible');

    // Obtener ID del evento recién creado (asumiendo que se muestra en data-id)
    let eventId;
    cy.contains(eventTitle)
      .parent()
      .invoke('attr', 'data-event-id')
      .then((id) => {
        eventId = id;
      });

    // Mover el evento a otro día (hoy + 1 día)
    const newDay = String(today.getDate() + 1).padStart(2, '0');
    const newDateStr = `${year}-${month}-${newDay}`;
    cy.get(`[data-testid="event-${eventId}"]`).trigger('dragstart');
    cy.get(`[data-testid="day-${newDateStr}"]`).trigger('drop');

    // Verificar que la llamada PUT fue realizada (mocking backend)
    cy.intercept('PUT', `/api/events/${eventId}`).as('updateEvent');
    cy.wait('@updateEvent').its('response.statusCode').should('eq', 200);

    // Confirmar que el evento se muestra en el nuevo día
    cy.get(`[data-testid="day-${newDateStr}"]`).within(() => {
      cy.contains(eventTitle).should('be.visible');
    });

    // Eliminar el evento
    cy.get(`[data-testid="event-${eventId}"]`).click();
    cy.get('[data-testid="btn-delete-event"]').click();

    // Verificar que la llamada DELETE fue realizada
    cy.intercept('DELETE', `/api/events/${eventId}`).as('deleteEvent');
    cy.wait('@deleteEvent').its('response.statusCode').should('eq', 200);

    // Confirmar desaparición del evento
    cy.contains(eventTitle).should('not.exist');
  });
});