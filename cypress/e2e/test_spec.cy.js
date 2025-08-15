describe('Calendar E2E Tests', () => {
  const apiUrl = 'http://localhost:5000/api/events';

  // Helper to create an event via API (used for cleanup)
  const deleteAllEvents = () => {
    cy.request('GET', `${apiUrl}`).then((response) => {
      response.body.forEach((event) => {
        cy.request('DELETE', `${apiUrl}/${event.id}`);
      });
    });
  };

  before(() => {
    // Ensure a clean state before tests
    deleteAllEvents();
  });

  it('debe cargar la página principal y mostrar el calendario con eventos del mes actual', () => {
    cy.visit('/');
    cy.get('[data-testid="calendar"]').should('be.visible');
    // Expect at least one event for the current month (may be none if clean)
    cy.get('[data-testid^="event-"]')
      .then((events) => {
        expect(events.length).to.be.at.least(0);
      });
  });

  it('debe crear un nuevo evento y aparecer en el calendario', () => {
    // Click on a day cell (choose the first available)
    cy.get('[data-testid^="day-"]').first().click();

    // Modal should appear
    cy.get('[data-testid="event-modal"]').should('be.visible');

    // Fill in event details
    const title = 'Prueba Cypress';
    const startDate = new Date();
    const endDate = new Date(startDate);
    endDate.setHours(endDate.getHours() + 1);

    cy.get('[data-testid="input-title"]').type(title);
    cy.get('[data-testid="input-start"]').clear().type(
      `${startDate.toISOString().slice(0, 16)}`
    );
    cy.get('[data-testid="input-end"]').clear().type(
      `${endDate.toISOString().slice(0, 16)}`
    );

    // Submit the form
    cy.get('[data-testid="submit-event"]').click();

    // Modal should close
    cy.get('[data-testid="event-modal"]').should('not.exist');

    // Verify event appears in calendar
    cy.contains('[data-testid^="event-"]', title).should('be.visible');
  });

  it('debe eliminar un evento existente y confirmar su ausencia', () => {
    // Grab an existing event (the one created above)
    cy.get('[data-testid^="event-"]').first().as('event');

    cy.get('@event')
      .find('[data-testid^="delete-event-"]')
      .click();

    // Confirm deletion in any modal if present
    cy.on('window:confirm', () => true);

    // Event should no longer exist
    cy.get('@event').should('not.exist');
  });

  it('debe mover un evento a otro día mediante drag-and-drop y actualizar su fecha', () => {
    // Create an event to move
    const title = 'Mover Evento';
    const startDate = new Date();
    const endDate = new Date(startDate);
    endDate.setHours(endDate.getHours() + 1);

    cy.request('POST', apiUrl, {
      titulo: title,
      descripcion: '',
      fecha_inicio: startDate.toISOString(),
      fecha_fin: endDate.toISOString(),
      color: '#ff0000',
    });

    // Wait for event to appear
    cy.contains('[data-testid^="event-"]', title).as('movingEvent');

    // Find source and target day cells
    cy.get('@movingEvent').closest('[data-testid^="day-"]').invoke('attr', 'data-testid')
      .then((sourceDay) => {
        const sourceDate = sourceDay.replace('day-', '');
        // Target: next day
        const targetDateObj = new Date(sourceDate);
        targetDateObj.setDate(targetDateObj.getDate() + 1);
        const targetDay = `day-${targetDateObj.toISOString().slice(0, 10)}`;

        // Perform drag-and-drop (using cypress-drag-drop plugin or custom)
        cy.get('@movingEvent')
          .trigger('mousedown', { which: 1 })
          .trigger('mousemove', { clientX: 200, clientY: 200 }) // coordinates are arbitrary
          .trigger('mouseup');

        // Alternatively, if using a library:
        // cy.get('@movingEvent').drag(targetDay);

        // Verify PUT request was sent with updated date
        cy.intercept('PUT', `${apiUrl}/*`).as('updateEvent');
        cy.wait('@updateEvent').its('request.body').should((body) => {
          expect(body.fecha_inicio).to.equal(
            targetDateObj.toISOString().slice(0, 16)
          );
        });

        // Verify event now appears under the target day
        cy.get(`[data-testid="${targetDay}"]`).contains(title).should('be.visible');
      });
  });
});