package org.gunnarkleiven.robotgenerator.parser.antlr.internal;

import org.eclipse.xtext.*;
import org.eclipse.xtext.parser.*;
import org.eclipse.xtext.parser.impl.*;
import org.eclipse.emf.ecore.util.EcoreUtil;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.common.util.Enumerator;
import org.eclipse.xtext.parser.antlr.AbstractInternalAntlrParser;
import org.eclipse.xtext.parser.antlr.XtextTokenStream;
import org.eclipse.xtext.parser.antlr.XtextTokenStream.HiddenTokens;
import org.eclipse.xtext.parser.antlr.AntlrDatatypeRuleToken;
import org.gunnarkleiven.robotgenerator.services.RobotgeneratorGrammarAccess;



import org.antlr.runtime.*;
import java.util.Stack;
import java.util.List;
import java.util.ArrayList;

@SuppressWarnings("all")
public class InternalRobotgeneratorParser extends AbstractInternalAntlrParser {
    public static final String[] tokenNames = new String[] {
        "<invalid>", "<EOR>", "<DOWN>", "<UP>", "RULE_STRING", "RULE_INT", "RULE_ID", "RULE_ML_COMMENT", "RULE_SL_COMMENT", "RULE_WS", "RULE_ANY_OTHER", "'('", "','", "')'", "';'", "'addRobot'", "'removeRobot'", "'moose'", "'mavic2pro'", "'op2'"
    };
    public static final int RULE_STRING=4;
    public static final int RULE_SL_COMMENT=8;
    public static final int T__19=19;
    public static final int T__15=15;
    public static final int T__16=16;
    public static final int T__17=17;
    public static final int T__18=18;
    public static final int T__11=11;
    public static final int T__12=12;
    public static final int T__13=13;
    public static final int T__14=14;
    public static final int EOF=-1;
    public static final int RULE_ID=6;
    public static final int RULE_WS=9;
    public static final int RULE_ANY_OTHER=10;
    public static final int RULE_INT=5;
    public static final int RULE_ML_COMMENT=7;

    // delegates
    // delegators


        public InternalRobotgeneratorParser(TokenStream input) {
            this(input, new RecognizerSharedState());
        }
        public InternalRobotgeneratorParser(TokenStream input, RecognizerSharedState state) {
            super(input, state);
             
        }
        

    public String[] getTokenNames() { return InternalRobotgeneratorParser.tokenNames; }
    public String getGrammarFileName() { return "InternalRobotgenerator.g"; }



     	private RobotgeneratorGrammarAccess grammarAccess;

        public InternalRobotgeneratorParser(TokenStream input, RobotgeneratorGrammarAccess grammarAccess) {
            this(input);
            this.grammarAccess = grammarAccess;
            registerRules(grammarAccess.getGrammar());
        }

        @Override
        protected String getFirstRuleName() {
        	return "Model";
       	}

       	@Override
       	protected RobotgeneratorGrammarAccess getGrammarAccess() {
       		return grammarAccess;
       	}




    // $ANTLR start "entryRuleModel"
    // InternalRobotgenerator.g:65:1: entryRuleModel returns [EObject current=null] : iv_ruleModel= ruleModel EOF ;
    public final EObject entryRuleModel() throws RecognitionException {
        EObject current = null;

        EObject iv_ruleModel = null;


        try {
            // InternalRobotgenerator.g:65:46: (iv_ruleModel= ruleModel EOF )
            // InternalRobotgenerator.g:66:2: iv_ruleModel= ruleModel EOF
            {
             newCompositeNode(grammarAccess.getModelRule()); 
            pushFollow(FOLLOW_1);
            iv_ruleModel=ruleModel();

            state._fsp--;

             current =iv_ruleModel; 
            match(input,EOF,FOLLOW_2); 

            }

        }

            catch (RecognitionException re) {
                recover(input,re);
                appendSkippedTokens();
            }
        finally {
        }
        return current;
    }
    // $ANTLR end "entryRuleModel"


    // $ANTLR start "ruleModel"
    // InternalRobotgenerator.g:72:1: ruleModel returns [EObject current=null] : ( (lv_commands_0_0= ruleCommand ) )* ;
    public final EObject ruleModel() throws RecognitionException {
        EObject current = null;

        EObject lv_commands_0_0 = null;



        	enterRule();

        try {
            // InternalRobotgenerator.g:78:2: ( ( (lv_commands_0_0= ruleCommand ) )* )
            // InternalRobotgenerator.g:79:2: ( (lv_commands_0_0= ruleCommand ) )*
            {
            // InternalRobotgenerator.g:79:2: ( (lv_commands_0_0= ruleCommand ) )*
            loop1:
            do {
                int alt1=2;
                int LA1_0 = input.LA(1);

                if ( ((LA1_0>=15 && LA1_0<=16)) ) {
                    alt1=1;
                }


                switch (alt1) {
            	case 1 :
            	    // InternalRobotgenerator.g:80:3: (lv_commands_0_0= ruleCommand )
            	    {
            	    // InternalRobotgenerator.g:80:3: (lv_commands_0_0= ruleCommand )
            	    // InternalRobotgenerator.g:81:4: lv_commands_0_0= ruleCommand
            	    {

            	    				newCompositeNode(grammarAccess.getModelAccess().getCommandsCommandParserRuleCall_0());
            	    			
            	    pushFollow(FOLLOW_3);
            	    lv_commands_0_0=ruleCommand();

            	    state._fsp--;


            	    				if (current==null) {
            	    					current = createModelElementForParent(grammarAccess.getModelRule());
            	    				}
            	    				add(
            	    					current,
            	    					"commands",
            	    					lv_commands_0_0,
            	    					"org.gunnarkleiven.robotgenerator.Robotgenerator.Command");
            	    				afterParserOrEnumRuleCall();
            	    			

            	    }


            	    }
            	    break;

            	default :
            	    break loop1;
                }
            } while (true);


            }


            	leaveRule();

        }

            catch (RecognitionException re) {
                recover(input,re);
                appendSkippedTokens();
            }
        finally {
        }
        return current;
    }
    // $ANTLR end "ruleModel"


    // $ANTLR start "entryRuleCommand"
    // InternalRobotgenerator.g:101:1: entryRuleCommand returns [EObject current=null] : iv_ruleCommand= ruleCommand EOF ;
    public final EObject entryRuleCommand() throws RecognitionException {
        EObject current = null;

        EObject iv_ruleCommand = null;


        try {
            // InternalRobotgenerator.g:101:48: (iv_ruleCommand= ruleCommand EOF )
            // InternalRobotgenerator.g:102:2: iv_ruleCommand= ruleCommand EOF
            {
             newCompositeNode(grammarAccess.getCommandRule()); 
            pushFollow(FOLLOW_1);
            iv_ruleCommand=ruleCommand();

            state._fsp--;

             current =iv_ruleCommand; 
            match(input,EOF,FOLLOW_2); 

            }

        }

            catch (RecognitionException re) {
                recover(input,re);
                appendSkippedTokens();
            }
        finally {
        }
        return current;
    }
    // $ANTLR end "entryRuleCommand"


    // $ANTLR start "ruleCommand"
    // InternalRobotgenerator.g:108:1: ruleCommand returns [EObject current=null] : ( ( (lv_commandType_0_0= ruleCommandType ) ) otherlv_1= '(' ( (lv_robotType_2_0= ruleRobotType ) ) otherlv_3= ',' ( (lv_robotName_4_0= ruleRobotName ) )? otherlv_5= ',' ( (lv_xValue_6_0= rulePositionValue ) )? otherlv_7= ',' ( (lv_yValue_8_0= rulePositionValue ) )? otherlv_9= ')' otherlv_10= ';' ) ;
    public final EObject ruleCommand() throws RecognitionException {
        EObject current = null;

        Token otherlv_1=null;
        Token otherlv_3=null;
        Token otherlv_5=null;
        Token otherlv_7=null;
        Token otherlv_9=null;
        Token otherlv_10=null;
        EObject lv_commandType_0_0 = null;

        Enumerator lv_robotType_2_0 = null;

        EObject lv_robotName_4_0 = null;

        EObject lv_xValue_6_0 = null;

        EObject lv_yValue_8_0 = null;



        	enterRule();

        try {
            // InternalRobotgenerator.g:114:2: ( ( ( (lv_commandType_0_0= ruleCommandType ) ) otherlv_1= '(' ( (lv_robotType_2_0= ruleRobotType ) ) otherlv_3= ',' ( (lv_robotName_4_0= ruleRobotName ) )? otherlv_5= ',' ( (lv_xValue_6_0= rulePositionValue ) )? otherlv_7= ',' ( (lv_yValue_8_0= rulePositionValue ) )? otherlv_9= ')' otherlv_10= ';' ) )
            // InternalRobotgenerator.g:115:2: ( ( (lv_commandType_0_0= ruleCommandType ) ) otherlv_1= '(' ( (lv_robotType_2_0= ruleRobotType ) ) otherlv_3= ',' ( (lv_robotName_4_0= ruleRobotName ) )? otherlv_5= ',' ( (lv_xValue_6_0= rulePositionValue ) )? otherlv_7= ',' ( (lv_yValue_8_0= rulePositionValue ) )? otherlv_9= ')' otherlv_10= ';' )
            {
            // InternalRobotgenerator.g:115:2: ( ( (lv_commandType_0_0= ruleCommandType ) ) otherlv_1= '(' ( (lv_robotType_2_0= ruleRobotType ) ) otherlv_3= ',' ( (lv_robotName_4_0= ruleRobotName ) )? otherlv_5= ',' ( (lv_xValue_6_0= rulePositionValue ) )? otherlv_7= ',' ( (lv_yValue_8_0= rulePositionValue ) )? otherlv_9= ')' otherlv_10= ';' )
            // InternalRobotgenerator.g:116:3: ( (lv_commandType_0_0= ruleCommandType ) ) otherlv_1= '(' ( (lv_robotType_2_0= ruleRobotType ) ) otherlv_3= ',' ( (lv_robotName_4_0= ruleRobotName ) )? otherlv_5= ',' ( (lv_xValue_6_0= rulePositionValue ) )? otherlv_7= ',' ( (lv_yValue_8_0= rulePositionValue ) )? otherlv_9= ')' otherlv_10= ';'
            {
            // InternalRobotgenerator.g:116:3: ( (lv_commandType_0_0= ruleCommandType ) )
            // InternalRobotgenerator.g:117:4: (lv_commandType_0_0= ruleCommandType )
            {
            // InternalRobotgenerator.g:117:4: (lv_commandType_0_0= ruleCommandType )
            // InternalRobotgenerator.g:118:5: lv_commandType_0_0= ruleCommandType
            {

            					newCompositeNode(grammarAccess.getCommandAccess().getCommandTypeCommandTypeParserRuleCall_0_0());
            				
            pushFollow(FOLLOW_4);
            lv_commandType_0_0=ruleCommandType();

            state._fsp--;


            					if (current==null) {
            						current = createModelElementForParent(grammarAccess.getCommandRule());
            					}
            					set(
            						current,
            						"commandType",
            						lv_commandType_0_0,
            						"org.gunnarkleiven.robotgenerator.Robotgenerator.CommandType");
            					afterParserOrEnumRuleCall();
            				

            }


            }

            otherlv_1=(Token)match(input,11,FOLLOW_5); 

            			newLeafNode(otherlv_1, grammarAccess.getCommandAccess().getLeftParenthesisKeyword_1());
            		
            // InternalRobotgenerator.g:139:3: ( (lv_robotType_2_0= ruleRobotType ) )
            // InternalRobotgenerator.g:140:4: (lv_robotType_2_0= ruleRobotType )
            {
            // InternalRobotgenerator.g:140:4: (lv_robotType_2_0= ruleRobotType )
            // InternalRobotgenerator.g:141:5: lv_robotType_2_0= ruleRobotType
            {

            					newCompositeNode(grammarAccess.getCommandAccess().getRobotTypeRobotTypeEnumRuleCall_2_0());
            				
            pushFollow(FOLLOW_6);
            lv_robotType_2_0=ruleRobotType();

            state._fsp--;


            					if (current==null) {
            						current = createModelElementForParent(grammarAccess.getCommandRule());
            					}
            					set(
            						current,
            						"robotType",
            						lv_robotType_2_0,
            						"org.gunnarkleiven.robotgenerator.Robotgenerator.RobotType");
            					afterParserOrEnumRuleCall();
            				

            }


            }

            otherlv_3=(Token)match(input,12,FOLLOW_7); 

            			newLeafNode(otherlv_3, grammarAccess.getCommandAccess().getCommaKeyword_3());
            		
            // InternalRobotgenerator.g:162:3: ( (lv_robotName_4_0= ruleRobotName ) )?
            int alt2=2;
            int LA2_0 = input.LA(1);

            if ( (LA2_0==RULE_STRING) ) {
                alt2=1;
            }
            switch (alt2) {
                case 1 :
                    // InternalRobotgenerator.g:163:4: (lv_robotName_4_0= ruleRobotName )
                    {
                    // InternalRobotgenerator.g:163:4: (lv_robotName_4_0= ruleRobotName )
                    // InternalRobotgenerator.g:164:5: lv_robotName_4_0= ruleRobotName
                    {

                    					newCompositeNode(grammarAccess.getCommandAccess().getRobotNameRobotNameParserRuleCall_4_0());
                    				
                    pushFollow(FOLLOW_6);
                    lv_robotName_4_0=ruleRobotName();

                    state._fsp--;


                    					if (current==null) {
                    						current = createModelElementForParent(grammarAccess.getCommandRule());
                    					}
                    					set(
                    						current,
                    						"robotName",
                    						lv_robotName_4_0,
                    						"org.gunnarkleiven.robotgenerator.Robotgenerator.RobotName");
                    					afterParserOrEnumRuleCall();
                    				

                    }


                    }
                    break;

            }

            otherlv_5=(Token)match(input,12,FOLLOW_8); 

            			newLeafNode(otherlv_5, grammarAccess.getCommandAccess().getCommaKeyword_5());
            		
            // InternalRobotgenerator.g:185:3: ( (lv_xValue_6_0= rulePositionValue ) )?
            int alt3=2;
            int LA3_0 = input.LA(1);

            if ( (LA3_0==RULE_INT) ) {
                alt3=1;
            }
            switch (alt3) {
                case 1 :
                    // InternalRobotgenerator.g:186:4: (lv_xValue_6_0= rulePositionValue )
                    {
                    // InternalRobotgenerator.g:186:4: (lv_xValue_6_0= rulePositionValue )
                    // InternalRobotgenerator.g:187:5: lv_xValue_6_0= rulePositionValue
                    {

                    					newCompositeNode(grammarAccess.getCommandAccess().getXValuePositionValueParserRuleCall_6_0());
                    				
                    pushFollow(FOLLOW_6);
                    lv_xValue_6_0=rulePositionValue();

                    state._fsp--;


                    					if (current==null) {
                    						current = createModelElementForParent(grammarAccess.getCommandRule());
                    					}
                    					set(
                    						current,
                    						"xValue",
                    						lv_xValue_6_0,
                    						"org.gunnarkleiven.robotgenerator.Robotgenerator.PositionValue");
                    					afterParserOrEnumRuleCall();
                    				

                    }


                    }
                    break;

            }

            otherlv_7=(Token)match(input,12,FOLLOW_9); 

            			newLeafNode(otherlv_7, grammarAccess.getCommandAccess().getCommaKeyword_7());
            		
            // InternalRobotgenerator.g:208:3: ( (lv_yValue_8_0= rulePositionValue ) )?
            int alt4=2;
            int LA4_0 = input.LA(1);

            if ( (LA4_0==RULE_INT) ) {
                alt4=1;
            }
            switch (alt4) {
                case 1 :
                    // InternalRobotgenerator.g:209:4: (lv_yValue_8_0= rulePositionValue )
                    {
                    // InternalRobotgenerator.g:209:4: (lv_yValue_8_0= rulePositionValue )
                    // InternalRobotgenerator.g:210:5: lv_yValue_8_0= rulePositionValue
                    {

                    					newCompositeNode(grammarAccess.getCommandAccess().getYValuePositionValueParserRuleCall_8_0());
                    				
                    pushFollow(FOLLOW_10);
                    lv_yValue_8_0=rulePositionValue();

                    state._fsp--;


                    					if (current==null) {
                    						current = createModelElementForParent(grammarAccess.getCommandRule());
                    					}
                    					set(
                    						current,
                    						"yValue",
                    						lv_yValue_8_0,
                    						"org.gunnarkleiven.robotgenerator.Robotgenerator.PositionValue");
                    					afterParserOrEnumRuleCall();
                    				

                    }


                    }
                    break;

            }

            otherlv_9=(Token)match(input,13,FOLLOW_11); 

            			newLeafNode(otherlv_9, grammarAccess.getCommandAccess().getRightParenthesisKeyword_9());
            		
            otherlv_10=(Token)match(input,14,FOLLOW_2); 

            			newLeafNode(otherlv_10, grammarAccess.getCommandAccess().getSemicolonKeyword_10());
            		

            }


            }


            	leaveRule();

        }

            catch (RecognitionException re) {
                recover(input,re);
                appendSkippedTokens();
            }
        finally {
        }
        return current;
    }
    // $ANTLR end "ruleCommand"


    // $ANTLR start "entryRuleRobotName"
    // InternalRobotgenerator.g:239:1: entryRuleRobotName returns [EObject current=null] : iv_ruleRobotName= ruleRobotName EOF ;
    public final EObject entryRuleRobotName() throws RecognitionException {
        EObject current = null;

        EObject iv_ruleRobotName = null;


        try {
            // InternalRobotgenerator.g:239:50: (iv_ruleRobotName= ruleRobotName EOF )
            // InternalRobotgenerator.g:240:2: iv_ruleRobotName= ruleRobotName EOF
            {
             newCompositeNode(grammarAccess.getRobotNameRule()); 
            pushFollow(FOLLOW_1);
            iv_ruleRobotName=ruleRobotName();

            state._fsp--;

             current =iv_ruleRobotName; 
            match(input,EOF,FOLLOW_2); 

            }

        }

            catch (RecognitionException re) {
                recover(input,re);
                appendSkippedTokens();
            }
        finally {
        }
        return current;
    }
    // $ANTLR end "entryRuleRobotName"


    // $ANTLR start "ruleRobotName"
    // InternalRobotgenerator.g:246:1: ruleRobotName returns [EObject current=null] : ( () ( (lv_value_1_0= RULE_STRING ) ) ) ;
    public final EObject ruleRobotName() throws RecognitionException {
        EObject current = null;

        Token lv_value_1_0=null;


        	enterRule();

        try {
            // InternalRobotgenerator.g:252:2: ( ( () ( (lv_value_1_0= RULE_STRING ) ) ) )
            // InternalRobotgenerator.g:253:2: ( () ( (lv_value_1_0= RULE_STRING ) ) )
            {
            // InternalRobotgenerator.g:253:2: ( () ( (lv_value_1_0= RULE_STRING ) ) )
            // InternalRobotgenerator.g:254:3: () ( (lv_value_1_0= RULE_STRING ) )
            {
            // InternalRobotgenerator.g:254:3: ()
            // InternalRobotgenerator.g:255:4: 
            {

            				current = forceCreateModelElement(
            					grammarAccess.getRobotNameAccess().getRobotNameAction_0(),
            					current);
            			

            }

            // InternalRobotgenerator.g:261:3: ( (lv_value_1_0= RULE_STRING ) )
            // InternalRobotgenerator.g:262:4: (lv_value_1_0= RULE_STRING )
            {
            // InternalRobotgenerator.g:262:4: (lv_value_1_0= RULE_STRING )
            // InternalRobotgenerator.g:263:5: lv_value_1_0= RULE_STRING
            {
            lv_value_1_0=(Token)match(input,RULE_STRING,FOLLOW_2); 

            					newLeafNode(lv_value_1_0, grammarAccess.getRobotNameAccess().getValueSTRINGTerminalRuleCall_1_0());
            				

            					if (current==null) {
            						current = createModelElement(grammarAccess.getRobotNameRule());
            					}
            					setWithLastConsumed(
            						current,
            						"value",
            						lv_value_1_0,
            						"org.eclipse.xtext.common.Terminals.STRING");
            				

            }


            }


            }


            }


            	leaveRule();

        }

            catch (RecognitionException re) {
                recover(input,re);
                appendSkippedTokens();
            }
        finally {
        }
        return current;
    }
    // $ANTLR end "ruleRobotName"


    // $ANTLR start "entryRulePositionValue"
    // InternalRobotgenerator.g:283:1: entryRulePositionValue returns [EObject current=null] : iv_rulePositionValue= rulePositionValue EOF ;
    public final EObject entryRulePositionValue() throws RecognitionException {
        EObject current = null;

        EObject iv_rulePositionValue = null;


        try {
            // InternalRobotgenerator.g:283:54: (iv_rulePositionValue= rulePositionValue EOF )
            // InternalRobotgenerator.g:284:2: iv_rulePositionValue= rulePositionValue EOF
            {
             newCompositeNode(grammarAccess.getPositionValueRule()); 
            pushFollow(FOLLOW_1);
            iv_rulePositionValue=rulePositionValue();

            state._fsp--;

             current =iv_rulePositionValue; 
            match(input,EOF,FOLLOW_2); 

            }

        }

            catch (RecognitionException re) {
                recover(input,re);
                appendSkippedTokens();
            }
        finally {
        }
        return current;
    }
    // $ANTLR end "entryRulePositionValue"


    // $ANTLR start "rulePositionValue"
    // InternalRobotgenerator.g:290:1: rulePositionValue returns [EObject current=null] : ( () ( (lv_value_1_0= RULE_INT ) ) ) ;
    public final EObject rulePositionValue() throws RecognitionException {
        EObject current = null;

        Token lv_value_1_0=null;


        	enterRule();

        try {
            // InternalRobotgenerator.g:296:2: ( ( () ( (lv_value_1_0= RULE_INT ) ) ) )
            // InternalRobotgenerator.g:297:2: ( () ( (lv_value_1_0= RULE_INT ) ) )
            {
            // InternalRobotgenerator.g:297:2: ( () ( (lv_value_1_0= RULE_INT ) ) )
            // InternalRobotgenerator.g:298:3: () ( (lv_value_1_0= RULE_INT ) )
            {
            // InternalRobotgenerator.g:298:3: ()
            // InternalRobotgenerator.g:299:4: 
            {

            				current = forceCreateModelElement(
            					grammarAccess.getPositionValueAccess().getPositionValueAction_0(),
            					current);
            			

            }

            // InternalRobotgenerator.g:305:3: ( (lv_value_1_0= RULE_INT ) )
            // InternalRobotgenerator.g:306:4: (lv_value_1_0= RULE_INT )
            {
            // InternalRobotgenerator.g:306:4: (lv_value_1_0= RULE_INT )
            // InternalRobotgenerator.g:307:5: lv_value_1_0= RULE_INT
            {
            lv_value_1_0=(Token)match(input,RULE_INT,FOLLOW_2); 

            					newLeafNode(lv_value_1_0, grammarAccess.getPositionValueAccess().getValueINTTerminalRuleCall_1_0());
            				

            					if (current==null) {
            						current = createModelElement(grammarAccess.getPositionValueRule());
            					}
            					setWithLastConsumed(
            						current,
            						"value",
            						lv_value_1_0,
            						"org.eclipse.xtext.common.Terminals.INT");
            				

            }


            }


            }


            }


            	leaveRule();

        }

            catch (RecognitionException re) {
                recover(input,re);
                appendSkippedTokens();
            }
        finally {
        }
        return current;
    }
    // $ANTLR end "rulePositionValue"


    // $ANTLR start "entryRuleCommandType"
    // InternalRobotgenerator.g:327:1: entryRuleCommandType returns [EObject current=null] : iv_ruleCommandType= ruleCommandType EOF ;
    public final EObject entryRuleCommandType() throws RecognitionException {
        EObject current = null;

        EObject iv_ruleCommandType = null;


        try {
            // InternalRobotgenerator.g:327:52: (iv_ruleCommandType= ruleCommandType EOF )
            // InternalRobotgenerator.g:328:2: iv_ruleCommandType= ruleCommandType EOF
            {
             newCompositeNode(grammarAccess.getCommandTypeRule()); 
            pushFollow(FOLLOW_1);
            iv_ruleCommandType=ruleCommandType();

            state._fsp--;

             current =iv_ruleCommandType; 
            match(input,EOF,FOLLOW_2); 

            }

        }

            catch (RecognitionException re) {
                recover(input,re);
                appendSkippedTokens();
            }
        finally {
        }
        return current;
    }
    // $ANTLR end "entryRuleCommandType"


    // $ANTLR start "ruleCommandType"
    // InternalRobotgenerator.g:334:1: ruleCommandType returns [EObject current=null] : ( ( () ( (lv_value_1_0= 'addRobot' ) ) ) | ( () ( (lv_value_3_0= 'removeRobot' ) ) ) ) ;
    public final EObject ruleCommandType() throws RecognitionException {
        EObject current = null;

        Token lv_value_1_0=null;
        Token lv_value_3_0=null;


        	enterRule();

        try {
            // InternalRobotgenerator.g:340:2: ( ( ( () ( (lv_value_1_0= 'addRobot' ) ) ) | ( () ( (lv_value_3_0= 'removeRobot' ) ) ) ) )
            // InternalRobotgenerator.g:341:2: ( ( () ( (lv_value_1_0= 'addRobot' ) ) ) | ( () ( (lv_value_3_0= 'removeRobot' ) ) ) )
            {
            // InternalRobotgenerator.g:341:2: ( ( () ( (lv_value_1_0= 'addRobot' ) ) ) | ( () ( (lv_value_3_0= 'removeRobot' ) ) ) )
            int alt5=2;
            int LA5_0 = input.LA(1);

            if ( (LA5_0==15) ) {
                alt5=1;
            }
            else if ( (LA5_0==16) ) {
                alt5=2;
            }
            else {
                NoViableAltException nvae =
                    new NoViableAltException("", 5, 0, input);

                throw nvae;
            }
            switch (alt5) {
                case 1 :
                    // InternalRobotgenerator.g:342:3: ( () ( (lv_value_1_0= 'addRobot' ) ) )
                    {
                    // InternalRobotgenerator.g:342:3: ( () ( (lv_value_1_0= 'addRobot' ) ) )
                    // InternalRobotgenerator.g:343:4: () ( (lv_value_1_0= 'addRobot' ) )
                    {
                    // InternalRobotgenerator.g:343:4: ()
                    // InternalRobotgenerator.g:344:5: 
                    {

                    					current = forceCreateModelElement(
                    						grammarAccess.getCommandTypeAccess().getAddRobotAction_0_0(),
                    						current);
                    				

                    }

                    // InternalRobotgenerator.g:350:4: ( (lv_value_1_0= 'addRobot' ) )
                    // InternalRobotgenerator.g:351:5: (lv_value_1_0= 'addRobot' )
                    {
                    // InternalRobotgenerator.g:351:5: (lv_value_1_0= 'addRobot' )
                    // InternalRobotgenerator.g:352:6: lv_value_1_0= 'addRobot'
                    {
                    lv_value_1_0=(Token)match(input,15,FOLLOW_2); 

                    						newLeafNode(lv_value_1_0, grammarAccess.getCommandTypeAccess().getValueAddRobotKeyword_0_1_0());
                    					

                    						if (current==null) {
                    							current = createModelElement(grammarAccess.getCommandTypeRule());
                    						}
                    						setWithLastConsumed(current, "value", lv_value_1_0, "addRobot");
                    					

                    }


                    }


                    }


                    }
                    break;
                case 2 :
                    // InternalRobotgenerator.g:366:3: ( () ( (lv_value_3_0= 'removeRobot' ) ) )
                    {
                    // InternalRobotgenerator.g:366:3: ( () ( (lv_value_3_0= 'removeRobot' ) ) )
                    // InternalRobotgenerator.g:367:4: () ( (lv_value_3_0= 'removeRobot' ) )
                    {
                    // InternalRobotgenerator.g:367:4: ()
                    // InternalRobotgenerator.g:368:5: 
                    {

                    					current = forceCreateModelElement(
                    						grammarAccess.getCommandTypeAccess().getRemoveRobotAction_1_0(),
                    						current);
                    				

                    }

                    // InternalRobotgenerator.g:374:4: ( (lv_value_3_0= 'removeRobot' ) )
                    // InternalRobotgenerator.g:375:5: (lv_value_3_0= 'removeRobot' )
                    {
                    // InternalRobotgenerator.g:375:5: (lv_value_3_0= 'removeRobot' )
                    // InternalRobotgenerator.g:376:6: lv_value_3_0= 'removeRobot'
                    {
                    lv_value_3_0=(Token)match(input,16,FOLLOW_2); 

                    						newLeafNode(lv_value_3_0, grammarAccess.getCommandTypeAccess().getValueRemoveRobotKeyword_1_1_0());
                    					

                    						if (current==null) {
                    							current = createModelElement(grammarAccess.getCommandTypeRule());
                    						}
                    						setWithLastConsumed(current, "value", lv_value_3_0, "removeRobot");
                    					

                    }


                    }


                    }


                    }
                    break;

            }


            }


            	leaveRule();

        }

            catch (RecognitionException re) {
                recover(input,re);
                appendSkippedTokens();
            }
        finally {
        }
        return current;
    }
    // $ANTLR end "ruleCommandType"


    // $ANTLR start "ruleRobotType"
    // InternalRobotgenerator.g:393:1: ruleRobotType returns [Enumerator current=null] : ( (enumLiteral_0= 'moose' ) | (enumLiteral_1= 'mavic2pro' ) | (enumLiteral_2= 'op2' ) ) ;
    public final Enumerator ruleRobotType() throws RecognitionException {
        Enumerator current = null;

        Token enumLiteral_0=null;
        Token enumLiteral_1=null;
        Token enumLiteral_2=null;


        	enterRule();

        try {
            // InternalRobotgenerator.g:399:2: ( ( (enumLiteral_0= 'moose' ) | (enumLiteral_1= 'mavic2pro' ) | (enumLiteral_2= 'op2' ) ) )
            // InternalRobotgenerator.g:400:2: ( (enumLiteral_0= 'moose' ) | (enumLiteral_1= 'mavic2pro' ) | (enumLiteral_2= 'op2' ) )
            {
            // InternalRobotgenerator.g:400:2: ( (enumLiteral_0= 'moose' ) | (enumLiteral_1= 'mavic2pro' ) | (enumLiteral_2= 'op2' ) )
            int alt6=3;
            switch ( input.LA(1) ) {
            case 17:
                {
                alt6=1;
                }
                break;
            case 18:
                {
                alt6=2;
                }
                break;
            case 19:
                {
                alt6=3;
                }
                break;
            default:
                NoViableAltException nvae =
                    new NoViableAltException("", 6, 0, input);

                throw nvae;
            }

            switch (alt6) {
                case 1 :
                    // InternalRobotgenerator.g:401:3: (enumLiteral_0= 'moose' )
                    {
                    // InternalRobotgenerator.g:401:3: (enumLiteral_0= 'moose' )
                    // InternalRobotgenerator.g:402:4: enumLiteral_0= 'moose'
                    {
                    enumLiteral_0=(Token)match(input,17,FOLLOW_2); 

                    				current = grammarAccess.getRobotTypeAccess().getMOOSEEnumLiteralDeclaration_0().getEnumLiteral().getInstance();
                    				newLeafNode(enumLiteral_0, grammarAccess.getRobotTypeAccess().getMOOSEEnumLiteralDeclaration_0());
                    			

                    }


                    }
                    break;
                case 2 :
                    // InternalRobotgenerator.g:409:3: (enumLiteral_1= 'mavic2pro' )
                    {
                    // InternalRobotgenerator.g:409:3: (enumLiteral_1= 'mavic2pro' )
                    // InternalRobotgenerator.g:410:4: enumLiteral_1= 'mavic2pro'
                    {
                    enumLiteral_1=(Token)match(input,18,FOLLOW_2); 

                    				current = grammarAccess.getRobotTypeAccess().getMAVIC2PROEnumLiteralDeclaration_1().getEnumLiteral().getInstance();
                    				newLeafNode(enumLiteral_1, grammarAccess.getRobotTypeAccess().getMAVIC2PROEnumLiteralDeclaration_1());
                    			

                    }


                    }
                    break;
                case 3 :
                    // InternalRobotgenerator.g:417:3: (enumLiteral_2= 'op2' )
                    {
                    // InternalRobotgenerator.g:417:3: (enumLiteral_2= 'op2' )
                    // InternalRobotgenerator.g:418:4: enumLiteral_2= 'op2'
                    {
                    enumLiteral_2=(Token)match(input,19,FOLLOW_2); 

                    				current = grammarAccess.getRobotTypeAccess().getOP2EnumLiteralDeclaration_2().getEnumLiteral().getInstance();
                    				newLeafNode(enumLiteral_2, grammarAccess.getRobotTypeAccess().getOP2EnumLiteralDeclaration_2());
                    			

                    }


                    }
                    break;

            }


            }


            	leaveRule();

        }

            catch (RecognitionException re) {
                recover(input,re);
                appendSkippedTokens();
            }
        finally {
        }
        return current;
    }
    // $ANTLR end "ruleRobotType"

    // Delegated rules


 

    public static final BitSet FOLLOW_1 = new BitSet(new long[]{0x0000000000000000L});
    public static final BitSet FOLLOW_2 = new BitSet(new long[]{0x0000000000000002L});
    public static final BitSet FOLLOW_3 = new BitSet(new long[]{0x0000000000018002L});
    public static final BitSet FOLLOW_4 = new BitSet(new long[]{0x0000000000000800L});
    public static final BitSet FOLLOW_5 = new BitSet(new long[]{0x00000000000E0000L});
    public static final BitSet FOLLOW_6 = new BitSet(new long[]{0x0000000000001000L});
    public static final BitSet FOLLOW_7 = new BitSet(new long[]{0x0000000000001010L});
    public static final BitSet FOLLOW_8 = new BitSet(new long[]{0x0000000000001020L});
    public static final BitSet FOLLOW_9 = new BitSet(new long[]{0x0000000000002020L});
    public static final BitSet FOLLOW_10 = new BitSet(new long[]{0x0000000000002000L});
    public static final BitSet FOLLOW_11 = new BitSet(new long[]{0x0000000000004000L});

}