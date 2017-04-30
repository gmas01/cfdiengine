package com.maxima.bbgum;

public class EventBlackBox implements EventElem {

    @Override
    public void inComming(EventController v, DatAction action) {
        v.handlerInComming(this, action);
    }

    @Override
    public void outComming(EventController v, DatAction action) {
        v.handlerOutComming(this, action);
    }

    @Override
    public void timeOut(EventController v, DatAction action) {
        v.handlerTimeOut(this, action);
    }

    @Override
    public boolean isFlowTerm(EventController v) {
        return v.handlerIsFlowTerm(this);
    }

    @Override
    public int getConclusion(EventController v) {
        return v.handlerGetConclusion(this);
    }
}