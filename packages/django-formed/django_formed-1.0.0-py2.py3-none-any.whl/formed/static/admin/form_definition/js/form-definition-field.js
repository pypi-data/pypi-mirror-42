/*global django, Formed, Vue, Sortable, console */
django.jQuery(function ($) {
    'use strict';
    var definitionFieldName = 'definition',
        components = {},
        defaultFieldType = 'CharField',
        defaultComponent = 'text-input',
        defaultProperties = {
            'label': String,
            'required': Boolean,
            'help_text': String
        },
        defaultWidgetAttributes = {
            'class': 'field'
        },
        newFieldTemplate = {
            'label': 'New field',
            'name': '',
            'type': defaultFieldType,
            'widget_attributes': {
                'placeholder': null
            },
            'help_text': null,
            'required': true
        },
        fieldTypes = {};

    Vue.config.debug = true;

    /**
     * Returns a list of all the field names in the given definition
     * @param {Array} definition
     * @returns {Array}
     */
    function getAllFieldNames(definition) {
        var names = [];
        $.each(definition, function (i, page) {
            $.each(page.fieldsets, function (i, fieldset) {
                $.each(fieldset.rows, function (i, row) {
                    $.each(row, function (i, field) {
                        names.push(field.name);
                    });
                });
            });
        });
        return names;
    }

    /**
     * Returns new unique field name for the given definition
     * @param {Array} definition
     * @param {String} [prefix] Optional argument to use as prefix. Defaults to 'field'.
     * @returns {String}
     */
    function getUniqueName(definition, prefix) {
        var names = getAllFieldNames(definition),
            i = names.length + 1,
            name;

        prefix = prefix || 'field';

        do {
            name = prefix + i;
            i++;
        } while (names.indexOf(name) >= 0);

        return name;
    }

    /**
     * Returns a new field object with a unique name for the given definition
     * @param {Array} definition
     * @returns {newFieldTemplate}
     */
    function getNewFieldObject(definition) {
        var field = $.extend(true, {}, newFieldTemplate),
            namePrefix = 'field';

        field.name = getUniqueName(definition, namePrefix);
        field.label += ' ' + field.name.slice(namePrefix.length);

        return field;
    }

    /**
     * Returns event handlers for a sortable instance
     * @param {*} context
     * @returns {{onStart: Function, onAdd: Function, onRemove: Function, onUpdate: Function, onEnd: Function}}
     */
    function getSortableEventHandlers(context) {
        return {
            /**
             * Dragging started, stores the source list
             * Executed in context of SOURCE list
             * @param {{oldIndex:Number,newIndex:Number,from:Element,item:Element}} event
             */
            'onStart': function (event) {
                var $from = $(event.from),
                    sourceList = context.fieldset ? context.fieldset.rows : context.row,
                    oldIndex = event.oldIndex;
                // console.info('onStart', event);

                if (!$from.hasClass('rows')) {
                    // it's a .fields list, store the source list and source index
                    // sourceList = context.row;// sourceList[$from.prevAll('.form-row').length - 1];
                    oldIndex = $(event.item).prevAll().length;
                }
                context.$root.sourceList = sourceList;
                context.$root.targetList = null;
                context.$root.oldIndex = oldIndex;
            },
            /**
             * Executed in context of TARGET list
             * @param event
             */
            'onAdd': function (event) {
                // console.info('onAdd', event);
                context.$root.newIndex = event.newIndex;
                context.$root.targetList = context.fieldset ? context.fieldset.rows : context.row;
            },
            /**
             * Element is removed from the list into another list.
             * Executed of context of SOURCE list
             * Sets a flag that the item has been removed from 'our' list.
             * @param {{oldIndex:Number,newIndex:Number}} event
             */
            'onRemove': function (event) {
                // console.info('onRemove', event);
            },
            'onUpdate': function (event) {
                // console.info('onUpdate', event);
            },
            /**
             * Dragging ended, handles moving within the same list
             * executed in context of SOURCE list
             * @param {{oldIndex:Number,newIndex:Number,item:Element,from:Element,to:Element}} event
             */
            'onEnd': function (event) {
                var targetList = context.$root.targetList,
                    oldIndex = context.$root.oldIndex,
                    newIndex = context.$root.newIndex || event.newIndex;

                if (!targetList) {
                    // determine target list:
                    targetList = context.fieldset ? context.fieldset.rows : context.row;
                }

                moveItem(context.$root.sourceList, oldIndex, newIndex, targetList);

                // Due to the nature of Vue and the Drag and drop handler the new item is rendered before the drag
                // action ends making the item appear twice when dragged between lists. Here we remove the 'clone':
                if (context.$root.sourceList !== targetList) {
                    window.setTimeout(function() {
                        $(event.item).remove();
                    }, 0);
                }
            }
        };
    }

    /**
     * Moves items to the specified index in the same or between lists.
     * @param {Array} source The source list.
     * @param {Number} oldIndex The index of the item in the source list.
     * @param {Number} newIndex The index of the item in the target list.
     * @param {Array} [target] The target list, defaults to the source list when not provided.
     */
    function moveItem(source, oldIndex, newIndex, target) {
        target = target || source;
        target.splice(newIndex, 0, source.splice(oldIndex, 1)[0]);
    }

    /**
     * Returns the value form an object using dot notation
     * @param {Object} object
     * @param {String} path
     * @returns {*}
     */
    function getPath(object, path) {
        return path.split('.').reduce(function (obj, key) {
            return obj ? obj[key] : obj;
        }, object);
    }

    /**
     * Returns the value as a safe 'slug'
     * @param {String} value
     * @returns {String}
     */
    function slugify(value) {
        return value.replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();
    }

    Vue.component('text-input', Vue.extend({
        'template': document.getElementById('text-input-template'),
        'props': ['field'],
        'computed': {
            'inputType': function () {
                var type = getPath(this, 'field.type') || defaultFieldType,
                    field = type ? fieldTypes[type] : null;

                return field ? getPath(field, 'component.type') || 'text' : 'text';
            }/*,
            'placeholder': function () {
                return getPath(this, 'field.widget_attributes.placeholder');
            }
            */
        }
    }));
    Vue.component('select-input', Vue.extend({
        'template': document.getElementById('select-input-template'),
        'props': ['field'],
        'computed': {
            'multiple': function () {
                return getPath(fieldTypes[this.field.type], 'component.multiple');
            }
        }
    }));
    Vue.component('multiple-choice-input', Vue.extend({
        'template': document.getElementById('multiple-choice-input-template'),
        'props': ['field'],
        'computed': {
            'fieldName': function () {
                return 'dummy-field-' + this.field.name;
            },
            'inputType': function () {
                return getPath(fieldTypes[this.field.type], 'component.type');
            }
        }
    }));
    Vue.component('textarea-input', Vue.extend({
        'template': document.getElementById('textarea-input-template'),
        'props': ['field']/*,
        'computed': {
            'placeholder': function () {
                return getPath(this, 'field.widget_attributes.placeholder');
            }
        }*/
    }));
    Vue.component('form-field', Vue.extend({
        'template': document.getElementById('form-field-template'),
        'props': ['field'],
        'computed': {
            'componentName': function () {
                var name;

                if (this.field) {
                    if (this.field.type === 'CharField' && this.field.widget === 'Textarea') {
                        name = 'textarea-input';
                    } else {
                        name = getPath(fieldTypes, this.field.type + '.component.name') || defaultComponent;
                    }
                }
                return name || defaultComponent;
            }
        },
        'methods': {
            'editField': function (event) {
                event.preventDefault();
                // this.$root.propertyPane('field', this.field);
                this.$root.$set('editField', this.field);
            },
            'deleteField': function (event) {
                var index = this.$parent.row.indexOf(this.field);

                event.preventDefault();
                if (window.confirm(Formed.i18n.confirmDeleteField)) {
                    this.$parent.row.splice(index, 1);
                }
            }
        }
    }));
    Vue.component('form-row', Vue.extend({
        'template': document.getElementById('form-row-template'),
        'props': ['row'],
        'methods': {
            'deleteRow': function (event) {
                var index = this.$parent.fieldset.rows.indexOf(this.row);

                event.preventDefault();
                if (window.confirm(Formed.i18n.confirmDeleteRow)) {
                    this.$parent.fieldset.rows.splice(index, 1);
                }
            },
            'addField': function (event) {
                var newField = getNewFieldObject(this.$root.definition); // $.extend({}, newFieldTemplate);

                event.preventDefault();
                this.row.push(newField);
                this.$root.propertyPane('field', newField);
            }
        },
        'ready': function () {
            Sortable.create(this.$el.querySelector('.sortable-items'), $.extend(true, {
                'group': 'fields',
                'draggable': '.form-field',
                'animation': 150,
                // 'handle': '.field-drag-handle',
                'dragoverBubble': true
            }, getSortableEventHandlers(this)));
        }
    }));
    Vue.component('form-fieldset', Vue.extend({
        'template': document.getElementById('form-fieldset-template'),
        'props': ['fieldset'],
        'methods': {
            'editFieldset': function (event) {
                event.preventDefault();
                this.$root.propertyPane('fieldset', this.fieldset);
            },
            'deleteFieldset': function (event) {
                var index = this.$parent.page.fieldsets.indexOf(this.fieldset);

                event.preventDefault();
                if (window.confirm(Formed.i18n.confirmDeleteFieldset)) {
                    this.$parent.page.fieldsets.splice(index, 1);
                }
            },
            'addRow': function (event) {
                event.preventDefault();
                this.fieldset.rows.push([
                    getNewFieldObject(this.$root.definition)  // $.extend({}, newFieldTemplate)
                ]);
            }
        },
        'ready': function () {
            // Handle sorting of rows within a fieldset
            Sortable.create(this.$el.querySelector('.sortable-items'), $.extend(true, {
                'group': 'rows',
                'draggable': '.form-row',
                'animation': 150,
                'handle': '.row-drag-handle'
            }, getSortableEventHandlers(this)));
        }
    }));
    Vue.component('form-page', Vue.extend({
        'template': document.getElementById('form-page-template'),
        'props': ['page'],
        'methods': {
            'editPage': function (event) {
                event.preventDefault();
                this.$root.propertyPane('page', this.page);
            },
            'deletePage': function (event) {
                var index = this.$parent.definition.indexOf(this.page);

                event.preventDefault();
                if (window.confirm(Formed.i18n.confirmDeletePage)) {
                    this.$parent.definition.splice(index, 1);
                }
            },
            'addFieldset': function (event) {
                var newFieldset = {
                    'legend': 'New fieldset',
                    'rows': []
                };

                event.preventDefault();
                this.page.fieldsets.push(newFieldset);
                this.$root.propertyPane('fieldset', newFieldset);
            }
        }
    }));
    Vue.component('form-editor', Vue.extend({
        'template': document.getElementById('form-editor-template'),
        'props': ['definition'],
        'methods': {
            'addPage': function (event) {
                event.preventDefault();
                this.definition.push({
                    'name': 'New page',
                    'fieldsets': []
                });
            }
        }
    }));

    Vue.component('field-properties', Vue.extend({
        'template': document.getElementById('field-properties-template'),
        'data': function () {
            return {
                'fieldCategories': Formed.fieldTypes,
                'fieldTypes': fieldTypes,
                'newChoice': ['', ''],
                'errors': {}
            };
        },
        'props': ['field'],
        'methods': {
            'close': function (event) {
                event.preventDefault();
                if (this.validate()) {
                    this.$root.editField = null;
                }
            },
            'validate': function () {
                var valid = true,
                    fields = {
                        'label': { 'required': true },
                        'name': { 'required': true }
                    },
                    fieldName, field, value;

                for (fieldName in fields) {
                    if (fields.hasOwnProperty(fieldName)) {
                        field = fields[fieldName];
                        value = this.$root.editField[fieldName];

                        if (field.required && value === '') {
                            this.$set('errors.' + fieldName, Formed.i18n.errorFieldRequired);
                            valid = false;
                        }
                    }
                }

                if (valid) {
                    this.$set('errors', {});
                }

                return valid;
            },
            'isValid': function () {
                var valid = true, key;
                for (key in this.errors) {
                    if (this.errors.hasOwnProperty(key)) {
                        valid = false;
                        break;
                    }
                }
                return valid;
            },
            'addChoice': function (event) {
                event.preventDefault();
                if (this.newChoice.reduce(function (p, c) { return p + c; }).length) {
                    if (this.$root.editField.hasOwnProperty('choices')) {
                        this.$root.editField.choices.push(this.newChoice);
                    } else {
                        // no choices property exists, $set() it to make it reactive:
                        this.$root.$set('editField.choices', [this.newChoice]);
                        // this.$root.$set('editField.name', 'foo');
                        // fix for not reactive choices property. We 'touch' the existing name property:
                        var old = this.$root.editField.name;
                        this.$root.editField.name = '';
                        this.$root.editField.name = old;
                    }
                    this.newChoice = ['', ''];
                }
            },
            'removeChoice': function (index) {
                this.$root.editField.choices.splice(index, 1);
            },
            'preFillNameValue': function () {
                if (this.$root.editField.name === '') {
                    this.$root.editField.name = slugify(this.$root.editField.label);
                }
            },
            'preFillChoiceValue': function () {
                if (this.newChoice[0] === '') {
                    this.newChoice[0] = slugify(this.newChoice[1]);
                }
            }
        }
    }));
    Vue.component('fieldset-properties', Vue.extend({
        'template': document.getElementById('fieldset-properties-template'),
        'props': ['fieldset'],
        'methods': {
            'close': function (event) {
                event.preventDefault();
                this.$root.editFieldset = null;
            }
        }
    }));
    Vue.component('page-properties', Vue.extend({
        'template': document.getElementById('page-properties-template'),
        'props': ['page'],
        'methods': {
            'close': function (event) {
                event.preventDefault();
                this.$root.editPage = null;
            }
        }
    }));

    $('.field-' + definitionFieldName).each(function () {
        var $fieldFormRow = $(this),
            $definitionField = $fieldFormRow.find('[name=' + definitionFieldName + ']'),
            fieldValue = $definitionField.val(),
            definition = [],
            editor;

        $definitionField.parent().toggleClass('hidden-definition-field', !Formed.formed_show_json_field);

        try {
            if (fieldValue) {
                definition = JSON.parse(fieldValue);
            }
        } catch (e) {
            window.alert('Could not parse JSON!');
            console.error(e);
        }

        $.each(definition, function (page_index, page) {
            $.each(page.fieldsets, function (fieldset_index, fieldset) {
                $.each(fieldset.rows, function (row_index, row) {
                    $.each(row, function (field_index, field) {
                        field.type = field.type || defaultFieldType;
                        field.required = !!field.required;
                        field.help_text = field.help_text || null;
                        field.widget_attributes = field.widget_attributes || {};
                    });
                });
            });
        });

        /*
         window.updateDefinition = function (sourceRow, index, target, targetRow) {
         moveItem(definition[0].fieldsets[0].rows[sourceRow], index, target, definition[0].fieldsets[0].rows[targetRow]);
         };
         */

        // flatten the categorised fieldTypes list:
        $.each(Formed.fieldTypes, function (group, fields) {
            $.each(fields, function (i, field) {
                fieldTypes[field.type] = field;
            });
        });

        $fieldFormRow.append(
            '<div>' +
            '<form-editor :definition="definition"></form-editor>' +
            '<field-properties :field="editField"></field-properties>' +
            '<fieldset-properties :fieldset="editFieldset"></fieldset-properties>' +
            '<page-properties :page="editPage"></page-properties>' +
            '</div>'
        );

        // $root:
        editor = new Vue({
            'el': this,
            'methods': {
                'propertyPane': function (objectType, object) {
                    var typeVariables = {
                            'field': 'editField',
                            'fieldset': 'editFieldset',
                            'page': 'editPage'
                        },
                        variable = typeVariables[objectType],
                        key;

                    // clear all:
                    for (key in typeVariables) {
                        if (typeVariables.hasOwnProperty(key)) {
                            this[typeVariables[key]] = null;
                        }
                    }

                    this[variable] = object;
                }
            },
            'data': {
                'definition': definition,
                // When we want to edit the properties of a field, we populate the $root.editField object:
                'editField': null,
                // When we want to edit the properties of a fieldset, we populate the $root.editFieldset object:
                'editFieldset': null,
                // When we want to edit the properties of a page, we populate the $root.editPage object:
                'editPage': null
            }// , 'components': components
        });

        editor.$watch('definition', function (oldValue, newValue) {
            /*
            $.each(newValue, function (page_index, page) {
                console.warn('page:', page_index, page.name);
                $.each(page.fieldsets, function (fieldset_index, fieldset) {
                    console.info('- fieldset', fieldset_index, fieldset.legend);
                    $.each(fieldset.rows, function (row_index, row) {
                        console.info('- - row', row_index);
                        $.each(row, function (field_index, field) {
                            console.info('- - - field', field_index, field.label);
                        });
                    });
                });
            });
            */
            $definitionField.val(JSON.stringify(newValue));
        }, {'deep': true});

        return editor;
    });
});
