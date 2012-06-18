Ext.BLANK_IMAGE_URL = 'resources/s.gif';


Ext.ns('Docs');

Docs.DocPanel = Ext.extend(Ext.Panel, {
    initEvents: function() {
        Docs.DocPanel.superclass.initEvents.call(this);
        this.body.on('click', this.onBodyClick, this);
    },
    initComponent: function() {
        var node = this.initialConfig.node,
            id   = this.id = 'DocPanel-' + node.name;
        
        Ext.apply(this, {
            id : id,
            title : node.name,
            autoScroll:true,
            layout: 'fit',
            margins: '0 10 10 10',
            cls: 'docpanel',
            html : this.getTpl(node),
            tbar: [
                { 
                    xtype: 'tbfill'
                }, { 
                    text: 'Inheritance',
                    listeners: {
                        click: this.onMenuClick,
                        scope: this
                    }
                }, {
                    text: 'Properties',
                    listeners: {
                        click: this.onMenuClick,
                        scope: this
                    }
                }, {
                    text: 'Methods',
                    listeners: {
                        click: this.onMenuClick,
                        scope: this
                    }
                }, {
                    text: 'Signals',
                    listeners: {
                        click: this.onMenuClick,
                        scope: this
                    }
                }
            ]
        });
        
        Docs.DocPanel.superclass.initComponent.call(this);
    },
    
    getTpl: function(node) {
        var me  = this,
            tpl = new Ext.XTemplate(
                '<h1>{clsName}</h1>',
                '{[this.formatInterfaces(values)]}',
                '<div class="x-clear"></div>',
                '<h2>Main Description</h2>',
                '<p class="main-information">{[this.formatDoc(values.mainDoc)]}</p>',
                '<hr/>',
                '{[this.formatProperties(values)]}',
                '<hr/>',
                '{[this.formatMethods(values)]}',
                '<hr/>' + 
                '{[this.formatSignals(values)]}',
                {
                    formatInterfaces: function(values) {
                        if(values && values.hasOwnProperty('interfaces') && Ext.isArray(values.interfaces) && values.interfaces.length > 0) {
                            var result = '<div class="inheritance res-block">' + 
                                            '<pre class="res-block-inner">' + 
                                            '<b>Inheritance</b>\n' + 
                                            values.clsName,
                                ifaces = values.interfaces,
                                i = 0,
                                len = ifaces.length,
                                nest = 1,
                                iface,
                                fnLine = function(value, nest) {
                                    var indent = new Array(nest).join("&nbsp;&nbsp;");
                                    return '\n' + indent +  '<img src="resources/images/elbow-end.gif" />' + value[0];
                                };
                            
                            for(; i < len; i++) {
                                iface = ifaces[i];
                                result += fnLine(iface, nest)
                            }
                            
                            return result += '</pre></div>';
                        }
                        
                        return '';
                    },
                    formatProperties: function(values) {
                        var result = '<div class="properties">' + me._generateTableOpen('Properties'),
                            rows = [];
                        if(values && values.hasOwnProperty('properties') && Ext.isArray(values.properties) && values.properties.length > 0) {
                            var props = values.properties,
                                len   = props.length,
                                i, prop;
                            
                            for(i = 0; i < len; i++) {
                                prop = props[i];
                                
                                rows.push(me._generateTableRow(prop.name, false, this.formatRefTypes(prop.type || 'void', false), prop.description, i % 2 == 0));
                            }
                            
                            rows.push(me._generateTableClose());
                            
                        } else {
                            rows.push('<tr><td class="content">No Properties</td></tr>');
                        }
                       
                        return result + rows.join("") + '</div>';
 
                    },
                    formatMethods: function(values) {
                        var result = '<div class="methods">' + me._generateTableOpen('Methods'),
                            rows = [];
                        if(values && values.hasOwnProperty('methods') && Ext.isArray(values.methods) && values.methods.length > 0) {
                            var meths = values.methods,
                                ilen   = meths.length,
                                meth, params, param, rType, desc, i, j, jlen;
                            
                            for(i = 0; i < ilen; i++) {
                                meth = meths[i];
                                desc = meth.description || '';
                                params = [];
                                rType = false;
                                
                                if(meth.parameters) {
                                    params = [];
                                    for(j = 0, jlen = meth.parameters.length; j < jlen; j++) {
                                        param = meth.parameters[j];
                                        params.push(this.formatRefTypes(param.name, param.type));
                                    }
                                }
                                
                                if(meth.returns) {
                                    rType = meth.returns.type
                                    if(meth.returns.description) {
                                        desc += '<br/><b>Returns: </b><br/>' + meth.returns.description;
                                    }
                                }
                                
                                rows.push(me._generateTableRow(meth.name, params, this.formatRefTypes('', rType), desc, i % 2 == 0));
                            }
                            rows.push(me._generateTableClose());
                            
                        } else {
                            rows.push('<tr><td class="content">No Methods</td></tr>');
                        }
                       
                        return result + rows.join("") + '</div>';
                    },
                    formatSignals: function(values) {
                        var result = '<div class="signals">' + me._generateTableOpen('Signals'),
                            rows = [];
                        if(values && values.hasOwnProperty('signals') && Ext.isArray(values.signals) && values.signals.length > 0) {
                            var sigs = values.signals,
                                len   = sigs.length,
                                i, sig;
                            
                            for(i = 0; i < len; i++) {
                                sig = sigs[i];
                                rows.push(me._generateTableRow(sig.name, false, false, sig.description, i % 2 == 0));
                            }
                            
                            rows.push(me._generateTableClose());
                            
                        } else {
                            rows.push('<tr><td class="content">No Signals</td></tr>');
                        }
                       
                        return result + rows.join("") + '</div>';
                    },
                    formatDoc: function(doc) {
                        doc = doc || '';
                        
                        return doc.replace(/\n/g, '<br/>');
                    },
                    formatRefTypes: function(name, type) {
                        if(!type || type.indexOf('ref:') < 0) {
                            if(!type || type === name) {
                                return name
                            }
                            return type + ' ' + name;
                        }
                        
                        var sRef = type.split('ref:');
                        
                        return '<span class="linkRef" ref="' + sRef[1] + '">' + sRef[1] + '</span>&nbsp;' + name;
                        
                    }
                }
            );
        
        return tpl.apply({
            clsName : node.fullname,
            mainDoc : node.description,
            interfaces: node.interfaces,
            properties: node.members && node.members.properties,
            methods: node.members && node.members.methods,
            signals: node.members && node.members.signals
        });
    },
    onMenuClick: function(btn, event) {
        // this scope is panel
        var el = this.body.child('div.' + btn.text.toLowerCase());
        if(el) {
            var top = (el.getOffsetsTo(this.body)[1]) + this.body.dom.scrollTop;
			this.body.scrollTo('top', top-25, {duration:.5});        
        }
    },
    
    onBodyClick: function(event, target) {
        var t = Ext.get(target);
        if(t.hasClass('row-expand')) {
            event.stopEvent();
            var trEl = t.findParent('.expandable', 3, true),
                descEl  = trEl.down('td.content div.description'),
                descExpandEl = trEl.down('td.content div.description-expanded');
           
            // somehow toggling with .show() or .hide() or .setVisible() does not work...
            if(descEl.isVisible()) {
               descEl.setStyle('display', 'none');
               descExpandEl.setStyle('display', 'block');
            } else {
               descEl.setStyle('display', 'block');
               descExpandEl.setStyle('display', 'none');
            }
        } else if(t.getAttributeNS('', 'ref')) {
            event.stopEvent();
            this.loadTab(t.getAttributeNS('', 'ref'))
        }
    },
    
    loadTab: function(nodeName) {
        var id = 'Doc-' + nodeName,
            tabPanel = Ext.getCmp('docs-center'),
            tab = this.getComponent(id);
        if(tab) {
            tabPanel.setActiveTab(tab);
        } else {
            Ext.Ajax.request({
                url: 'data/' + id + '.json',
                success: function(response, con) {
                    var node = Ext.decode(response.responseText),
                        tabPanel = Ext.getCmp('docs-center'),
                        docPanel = new Docs.DocPanel({
                            node : node
                        });
                    tabPanel.add(docPanel).show();
                },
                failure: function() {
                    alert('Something went wrong loading the data');
                }
            });
        }
    },
    
    _generateTableOpen: function(type) {
        var table = '<table class="member-table">' +
                        '<thead>' + 
                            '<th colspan="2">' + type + '</th>' +
                         '</thead>' +
                         '<tbody>';
        
        return table;
    },
    
    _generateTableRow: function(elName, elParams, elReturns, elDesc, altRow) {
        var strLen = 150,
            trCls = altRow ? 'alt ' : '';
        
        if(elDesc && elDesc.length > strLen) {
            sdesc = elDesc.substr(0, strLen) + '...';
            ldesc = elDesc;
            micon = '<a href="#expand" class="row-expand">&nbsp;</a>';
            trCls += 'expandable';
        } else {
            sdesc = elDesc;
            ldesc = '';
            micon = '&nbsp';
        }
        
        if(Ext.isArray(elParams)) {
            elName = '<b>' + elName + '(</b> <code>' + (elParams.join(', ')) + ' </code><b>)</b>';
        } else {
            elName = '<b>' + elName + '</b>';   
        }
        
        if(elReturns) {
            elName += ' : ' + elReturns;
        }
        
        return '<tr class="' + trCls + '">' + 
                '<td class="micon">' + micon + '</td>' + 
                '<td class="content">' + 
                    elName + 
                    '<br/>' + 
                    '<div class="description">' + sdesc + '</div>' + 
                    '<div class="description-expanded">' + ldesc.replace(/\n/g, '<br/>') + '</div>' + 
                '</td>' + 
               '</tr>';
    },

    _generateTableClose: function() {
        return '</tbody></table>';
    }
});

Docs.Viewport = Ext.extend(Ext.Viewport, {
    initComponent: function() {
    
        var TreeLoader = new Ext.tree.TreeLoader({
            dataUrl:'data/tree.json',
            requestMethod : 'GET',
            processResponse : function(response, node, callback) {
                var json = response.responseText;
                try {
                  var o = Ext.decode(json)
                  node.beginUpdate();
                  for(var i=0, len=o.length; i<len; i++) {
                    var n = this.createNode(o[i]);
                    
                    if (n) {
                      node.appendChild(n);
                    }
                  }

                  node.endUpdate();

                  if(typeof callback == "function") {
                    callback(this, node);
                  }
                }
                catch (e) {
                  console.log("error", e)
                  this.handleFailure(response);
                }
              }

        });
        
        var AsyncTreeLoader = new Ext.tree.AsyncTreeNode({
            text:'Gtk-RootNode',
            id:'root',
            expanded:true
        });
    
        Ext.apply(this, {
            layout: 'border',
            defaults: {
                activeItem: 0
            },
            items: [{
                region: 'north',
                html: '<h1 class="x-panel-header">pyGtk3Docs - inofficial documentation</h1>',
                autoHeight: true,
                border: false,
                margins: '0 0 5 0'
            }, {
                region: 'west',
                collapsible: true,
                title: 'Navigation',
                xtype: 'treepanel',
                width: 200,
                autoScroll: true,
                split: false,
                loader: TreeLoader,
                root : AsyncTreeLoader,
                rootVisible: false,
                listeners: {
                    click: this.onNodeClick
                }
            }, {
                region: 'center',
                xtype: 'tabpanel',
                id: 'docs-center',
                plugins: new Ext.ux.TabCloseMenu(),
                defaults : {
                    closable: true
                },
                items: {
                    title: 'Welcome',
                    closable: false,
                    html: 'Welcome to the PyGtk3 inofficial documentation project'
                }
            }]
        });
        
        
        Docs.Viewport.superclass.initComponent.call(this);
    },
    
    onNodeClick: function(node, event) {
        if(!node.isLeaf()) {
            node.toggle();
        } else {
            Ext.Ajax.request({
                url: 'data/Doc-' + node.text + '.json',
                success: function(response, con) {
                    var node = Ext.decode(response.responseText),
                        tabPanel = Ext.getCmp('docs-center'),
                        docPanel = new Docs.DocPanel({
                            node : node
                        });
                    tabPanel.add(docPanel).show();
                },
                failure: function() {
                    alert('Something went wrong loading the data');
                }
            });
        }
    }
});

Ext.onReady(function(){
    c = console.log;
    Ext.QuickTips.init();
    
    var app = new Docs.Viewport();    
    
});
