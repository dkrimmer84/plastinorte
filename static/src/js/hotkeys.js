odoo.define('plastinorte', function (require) {
	"use strict";

	// Se importan los modulos necesarios
	var core = require('web.core');
	var models = require('point_of_sale.models');
	var session = require('web.session');
	var PosDB = require('point_of_sale.DB');
	var gui = require('point_of_sale.gui');
	var chrome = require('point_of_sale.chrome');
	var ajax = require('web.ajax');
	var Model = require('web.Model');
	var data = require('web.data');
	var PosBaseWidget = require('point_of_sale.BaseWidget');
	var Screens = require('point_of_sale.screens');

	var QWeb = core.qweb;
	var _t = core._t;


	Screens.PaymentScreenWidget.include({
		click_paymentmethods : function(id){
			var self = this;

			var cashregister = null;
	        for ( var i = 0; i < this.pos.cashregisters.length; i++ ) {
	            if ( this.pos.cashregisters[i].journal_id[0] === id ){
	                cashregister = this.pos.cashregisters[i];
	                break;
	            }
	        }

	        if( cashregister.journal != undefined ){

	        	if(cashregister.journal.type != 'cash' ){
	        		Mousetrap.unbind('return');

        			this.gui.show_popup('confirm',{
		                title: _t('Esta seguro que quiere realizar una venta con:'),
		                body: cashregister.journal_id[ 1 ] + " ?",
		                confirm: function() {
		                    self.pos.get_order().add_paymentline( cashregister );
					        self.reset_input();
					        self.render_paymentlines();

					        var _super_posmodel = models.PosModel.prototype;
					        _super_posmodel.eventReturn();
		                },
		                cancel : function(){
		                	var _super_posmodel = models.PosModel.prototype;
					        _super_posmodel.eventReturn();
		                }
		            });

        			Mousetrap.bindGlobal('esc', function(){
        				console.log('Nuevos eventos esc');

						if($('.popup-password').is(":visible")){
			    			var cancel = $('div.popup-password > div.centered > .cancel');
							cancel.click();
							return;

			    		}

			    		if($('.popup-confirm').is(":visible")){
			    			return;
			    		}

						if( $('.back').is(":visible") ){
							$('.back').click();

							return;
						}

					});


	        	} else {
	        		this.pos.get_order().add_paymentline( cashregister );
			        this.reset_input();
			        this.render_paymentlines()
	        	}


	        }



		}
	});

	/*var _super_posmodel = models.PosModel.prototype;
	models.PosModel = models.PosModel.extend({
		initialize: function(session, attributes) {
	    	var self = this;
	    	_super_posmodel.initialize.call(this,session,attributes);

	    	console.log('La herenciaaaaaaaa');

	    	$(document).ready(function(){
				Mousetrap.bindGlobal('esc', function(){
		    		console.log('Escapeeeee');
		    	});

			});
	    	
	    	

	    }

	});*/

	/*Screens.PaymentScreenWidget = Screens.PaymentScreenWidget.extend({
		click_paymentmethods : function(){
			console.log('Herencia...');
		}
	});*/


	/*console.log('ENTRA TESTTTTTT', Screens);

	var _super_posmodel = models.PosModel.prototype;
	models.PosModel = models.PosModel.extend({
	    initialize: function(session, attributes) {
	    	var self = this;
	    	_super_posmodel.initialize.call(this,session,attributes);
	    	


	    },

	});*/


 });
