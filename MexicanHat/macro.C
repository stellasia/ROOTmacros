/*
  Evolution of "Higgs" potential as x**2 term becomes negative.

  Usage: root macro.C
*/


void macro() {
    TF1 *function = new TF1("function", 
			    "[0]*pow(x,2) + pow(x,4)", 
			    -5, 5);
  
    TCanvas *c = new TCanvas("c", "c", 800, 600);
    c->SetGrid();
    TH1F *histo_dummy;
    TLatex mylatex;
    char buffer[200];

    double v = 2; // initial value for the x**2 parameter in function
    for (int i=0; i<20; i++) {
	histo_dummy = c->DrawFrame(-3, -1.2, 3, 0.8);
	histo_dummy->SetXTitle("x");
	histo_dummy->SetYTitle("f(x)");

	function->SetParameter(0, v);
	function->Draw("same");

	mylatex.SetNDC(1);
	mylatex.DrawLatex(0.15,0.17,"f(x) = v#timesx^{2} + x^{4}");
	sprintf(buffer, "v=%2.1f", v);
	mylatex.DrawLatex(0.15,0.11,buffer);

	c->SaveAs("result.gif+20");
	v-=0.2;
    }
    c->SaveAs("result.gif++");
}
