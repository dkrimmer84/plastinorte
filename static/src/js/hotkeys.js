odoo.define('plastinorte', function (require) {
	"use strict";

	// Se importan los modulos necesarios
	var core = require('web.core');
	var models = require('point_of_sale.models');
	var Screens = require('point_of_sale.screens');

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

					        $('.paymentmethod').removeClass('payment_selected');
		                },
		                cancel : function(){
		                	var _super_posmodel = models.PosModel.prototype;
					        _super_posmodel.eventReturn();
		                }
		            });

        			Mousetrap.bindGlobal('esc', function(){
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

	var _super_posmodel = models.PosModel.prototype;
	models.PosModel = models.PosModel.extend({
		cashregisters2 : undefined,

		initialize: function(session, attributes) {
	    	var self = this;
	    	_super_posmodel.initialize.call(this,session,attributes);

	    },

	    eventReturn : function(){
	    	var self = this;

	    	Mousetrap.bindGlobal('return', function( e ){
				if($('.popup-password').is(":visible")){
	    			var confirm = $('div.popup-password > div.centered > .confirm');
					confirm.click();
					return;
	    		}

				if( ! $('.next').is(":visible") ){
					if( $('.searchbox > input').is(":focus") ){
						$('.searchbox > input').blur();
					} else {
						var product_selected = $('.product').hasClass('product_selected');

						if( product_selected ){
							$('.product.product_selected').click();
							$('.product').removeClass('product_selected');

							return;
						}
					}
					
				} else {
					if($('.print').is(":visible")){
						$('.next').click();
						return;
					}

					var payment_selected = $('.payment_selected');
					if( payment_selected.length > 0 ){
						var payment_type = payment_selected.data('type');

        				if( payment_type  != 'cash' ){
        					e.preventDefault();
        					return;
        				} else {
        					payment_selected.click();
        					$('.paymentmethod').removeClass('payment_selected');
							e.preventDefault();
							return;
        				}
					}
				}
			});
	    },
	});
 });