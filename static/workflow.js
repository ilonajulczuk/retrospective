
$(function(){

        function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                                var cookie = jQuery.trim(cookies[i]);
                                // Does this cookie string begin with the name we want?
                                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                        break;
                                }
                        }
                }
                return cookieValue;
        }

        var csrftoken = getCookie('csrftoken');
        function csrfSafeMethod(method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
                crossDomain: false, // obviates need for sameOrigin test
                beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type)) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                }
        });

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

        // The collection of entries is backed by *localStorage* instead of a remote
        // server.
        var EntryList = Backbone.Collection.extend({
                model: Entry,

            localStorage: new Backbone.LocalStorage("entries-backbone1"),

            skippable: function() {
                    return this.where({skippable: true});
            },

            remaining: function() {
                    return this.where({skippable: false});
            },

            nextOrder: function() {
                    if (!this.length) return 1;
                    return this.last().get('order') + 1;
            },

            comparator: 'order'

        });

        var forms = [];
        var Entries = new EntryList;
        forms.push(Entries);

        // Sidebox View
        var SideboxView = Backbone.View.extend({
                el: $("#sidebox"),

            template: _.template($('#sidebox-template').html()),
            multiple: false,
            numberOfFields: 1,
            events: {
                    "click #save-workflow": "saveWorkflow",
                    "click #discard-workflow": "discardWorkflow",
                    "click #new-workflow": "startNewWorkflow",
                    "click #fields-single": "setFieldsSingle",
                    "click #fields-multiple": "setFieldsMultiple",
                    "change #fields-count": "changeNumberOfFields"
            },

            startNewWorkflow: function() {
                    alert("We'll start shortly");
            },

            setFieldsSingle: function() {
                    this.multiple = false;
                    this.render();
                    this.changeNumberOfFields();
            },

            setFieldsMultiple: function() {
                    this.multiple = true;
                    this.render();
                    this.changeNumberOfFields();
            },

            changeNumberOfFields: function(newNumber) {
                if(newNumber == null) {
                        newNumber = $("#fields-count").val();
                        if(newNumber == undefined) {
                                newNumber = 1;
                        }
                        this.numberOfFields = newNumber;
                }
                else {
                        this.numberOfFields = newNumber.target.value;
                }
                console.log(this.numberOfFields);
            },

            saveWorkflow: function() {
                    $.ajax({
                            type: "POST",
                            url: '/core/workflow/save',
                            dataType: "json",
                            data: {
                                    number_of_forms: _.size(Entries),
                                    forms:  JSON.stringify(_.map(forms, function(entries) {
                                            entriesInfo = entries.map(function(entry) {
                                            return {
                                                    title: entry.get("title"),
                                                inputType: entry.get("inputType"),
                                                skippable: entry.get("skippable")
                                            };
                                            });
                                            return {data: entriesInfo};

                                    })),
                                    title: $("#workflow-name").val()
                            }
                    })
                    .error(function(data) {
                    })
                    .success(function(data) {
                    })
            },

            discardWorkflow: function() {
                    $.ajax({
                            type: "POST",
                            url: '/core/workflow/delete',
                            dataType: "json",
                            data: {
                                    title: $("#workflow-name").val()
                            }
                    })
                    .error(function(data) {
                    })
                    .success(function(data) {
                    })
            },

            initialize: function() {
                    this.listenTo(Entries, 'all', this.render);
                    this.sidebox = $('#sidebox');
            },

            // Re-rendering the App just means refreshing the statistics -- the rest
            // of the app doesn't change.
            render: function() {
                    this.$el.html(this.template({multiple: this.multiple}));
                    return this;
            }
        });

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
            currentEntryNumber: 0,
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

            showPreviousEntry: function() {
                   console.log("oh previous entry");
                   if(this.currentEntryNumber > 0) {
                           Entries.stopListening();
                           Sidebox.stopListening(Entries);
                           Entries = forms[this.currentEntryNumber - 1];
                           Sidebox.listenTo(Entries, 'all', Sidebox.render);
                           this.currentEntryNumber -= 1;
                   }

                   this.clearViewOfAll();
                   this.addAll();
                   this.render();
                   this.listenTo(Entries, 'add', this.addOne);
                   this.listenTo(Entries, 'reset', this.addAll);
                   this.listenTo(Entries, 'all', this.render);
            },

            showNextEntry: function() {
                   console.log("next entry is comming");
                    if(this.currentEntryNumber + 1 == _.size(forms)) {
                           Entries.stopListening();
                           Sidebox.stopListening(Entries);
                           Entries = new EntryList();
                           Sidebox.listenTo(Entries, 'all', Sidebox.render);
                           forms.push(Entries);
                           console.log(Entries);
                   }
                   else {
                           Entries = forms[this.currentEntryNumber + 1]
                   }
                   this.currentEntryNumber += 1;
                   this.clearViewOfAll();
                   this.addAll();
                   this.render();
                   this.listenTo(Entries, 'add', this.addOne);
                   this.listenTo(Entries, 'reset', this.addAll);
                   this.listenTo(Entries, 'all', this.render);
            },

            // At initialization we bind to the relevant events on the `Entries`
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

                            this.footer.html(
                                    this.statsTemplate(
                                            {
                                                    skippable: skippable,
                                                    remaining: remaining
                                            }
                                     )
                            );

                    } else {
                            this.main.hide();
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
                    console.log("create on enter");
                    if (e.keyCode != 13) return;
                    if (!this.input.val()) return;
                    Entries.create({
                          title: this.input.val(),
                          inputType: this.valueType.val()
                    });
                    console.log("Oh, new entry should be created");
                    this.input.val('');
            },

            // Clear all skippable todo items, destroying their models.
            clearCompleted: function() {
                    _.invoke(Entries.skippable(), 'destroy');
                    return false;
            },

            clearViewOfAll: function() {
                    this.$("#todo-list").html("");
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

        Sidebox = new SideboxView();
        $("#sidebox").html(Sidebox.render().el);
        // Finally, we kick things off by creating the **App**.
        var App = new AppView;

});
