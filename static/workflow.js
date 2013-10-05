
$(function(){

  var Entry = Backbone.Model.extend({

    // Default attributes for the entry item.
    defaults: function() {
      return {
        title: "empty entry...",
        order: Entries.nextOrder(),
        skippable: false,
        inputType: "Small input"
      };
    },

    // Toggle the `skippable` state of this todo item.
    toggle: function() {
      this.save({skippable: !this.get("skippable")});
    }

  });

  // Todo Collection
  // ---------------

  // The collection of todos is backed by *localStorage* instead of a remote
  // server.
  var EntryList = Backbone.Collection.extend({

    // Reference to this collection's model.
    model: Entry,

    // Save all of the todo items under the `"todos-backbone"` namespace.
    localStorage: new Backbone.LocalStorage("entries-backbone1"),

    // Filter down the list of all todo items that are finished.
    skippable: function() {
      return this.where({skippable: true});
    },

    // Filter down the list to only todo items that are still not finished.
    remaining: function() {
      return this.where({skippable: false});
    },

    // We keep the Todos in sequential order, despite being saved by unordered
    // GUID in the database. This generates the next order number for new items.
    nextOrder: function() {
      if (!this.length) return 1;
      return this.last().get('order') + 1;
    },

    // Todos are sorted by their original insertion order.
    comparator: 'order'

  });

  // Create our global collection of **Todos**.
  var Entries = new EntryList;

  // Todo Item View
  // --------------

  // The DOM element for a todo item...
  var EntryView = Backbone.View.extend({

    //... is a list tag.
    tagName:  "li",

    // Cache the template function for a single item.
    template: _.template($('#item-template').html()),

    // The DOM events specific to an item.
    events: {
      "click .toggle"   : "toggleSkippable",
      "dblclick .view"  : "edit",
      "click a.destroy" : "clear",
      "keypress .edit"  : "updateOnEnter",
      "blur .edit"      : "close"
    },

    // The TodoView listens for changes to its model, re-rendering. Since there's
    // a one-to-one correspondence between a **Todo** and a **TodoView** in this
    // app, we set a direct reference on the model for convenience.
    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
    },

    // Re-render the titles of the entry item.
    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      this.$el.toggleClass('skippable', this.model.get('skippable'));
      this.input = this.$('.edit');
      return this;
    },

    // Toggle the `"skippable"` state of the model.
    toggleSkippable: function() {
      this.model.toggle();
    },

    // Switch this view into `"editing"` mode, displaying the input field.
    edit: function() {
      this.$el.addClass("editing");
      this.input.focus();
    },

    // Close the `"editing"` mode, saving changes to the todo.
    close: function() {
      var value = this.input.val();
      if (!value) {
        this.clear();
      } else {
        this.model.save({title: value});
        this.$el.removeClass("editing");
      }
    },

    // If you hit `enter`, we're through editing the item.
    updateOnEnter: function(e) {
      if (e.keyCode == 13) this.close();
    },

    // Remove the item, destroy the model.
    clear: function() {
      this.model.destroy();
    }

  });

  // Our overall **AppView** is the top-level piece of UI.
  var AppView = Backbone.View.extend({

    // Instead of generating a new element, bind to the existing skeleton of
    // the App already present in the HTML.
    el: $("#todoapp"),

    // Our template for the line of statistics at the bottom of the app.
    statsTemplate: _.template($('#stats-template').html()),

    // Delegated events for creating new items, and clearing completed ones.
    events: {
      "keypress #new-todo":  "createOnEnter",
      "click #clear-completed": "clearCompleted",
      "click #toggle-all": "toggleAllComplete",
      "click #save-entries": "saveEntries",
      "click #previous-entry": "showPreviousEntry",
      "click #next-entry": "showNextEntry"

    },

    // At initialization we bind to the relevant events on the `Todos`
    // collection, when items are added or changed. Kick things off by
    // loading any preexisting todos that might be saved in *localStorage*.
    initialize: function() {

      this.input = this.$("#new-todo");
      this.valueType = this.$("#type-of-value");
      this.allCheckbox = this.$("#toggle-all")[0];

      this.listenTo(Entries, 'add', this.addOne);
      this.listenTo(Entries, 'reset', this.addAll);
      this.listenTo(Entries, 'all', this.render);

      this.footer = this.$('footer');
      this.main = $('#main');

      Entries.fetch();
    },

    // Re-rendering the App just means refreshing the statistics -- the rest
    // of the app doesn't change.
    render: function() {
      var skippable = Entries.skippable().length;
      var remaining = Entries.remaining().length;

      if (Entries.length) {
        this.main.show();
        this.footer.show();
        this.footer.html(this.statsTemplate({skippable: skippable, remaining: remaining}));
      } else {
        this.main.hide();
        this.footer.hide();
      }

      this.allCheckbox.checked = !remaining;
    },

    // Add a single todo item to the list by creating a view for it, and
    // appending its element to the `<ul>`.
    addOne: function(entry) {
      var view = new EntryView({model: entry});
      this.$("#todo-list").append(view.render().el);
    },

    // Add all items in the **Todos** collection at once.
    addAll: function() {
      Entries.each(this.addOne, this);
    },

    // If you hit return in the main input field, create new **Todo** model,
    // persisting it to *localStorage*.
    createOnEnter: function(e) {
      if (e.keyCode != 13) return;
      if (!this.input.val()) return;
      Entries.create({title: this.input.val(), inputType: this.valueType.val()});
      this.input.val('');
    },

    // Clear all skippable todo items, destroying their models.
    clearCompleted: function() {
      _.invoke(Entries.skippable(), 'destroy');
      return false;
    },

    toggleAllComplete: function () {
      var skippable = this.allCheckbox.checked;
      Entries.each(function (entry) { entry.save({'skippable': skippable}); });
    },

    saveEntries: function () {
        // send message via api call that we need to save of this stuff
        alert("Your Entry Set has been saved!");
    }
  });

  // Finally, we kick things off by creating the **App**.
  var App = new AppView;

});
