import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

/** Stateless policy engine. Protocol: six newline-delimited validated scalars. */
public final class RegistryPolicy {
    static List<String> assess(int status, boolean name, boolean city, boolean state, boolean cnae) {
        var issues = new ArrayList<String>();
        if (status != 2) issues.add("not_active");
        if (!name) issues.add("missing_razao_social");
        if (!city) issues.add("missing_municipio");
        if (!state) issues.add("missing_uf");
        if (!cnae) issues.add("missing_cnae_fiscal");
        return List.copyOf(issues);
    }
    static boolean flag(String value) {
        if (!"true".equals(value) && !"false".equals(value)) throw new IllegalArgumentException("Invalid boolean");
        return Boolean.parseBoolean(value);
    }
    static boolean validCnpj(String value) {
        if (value == null || !value.matches("[0-9]{14}") || value.chars().distinct().count() == 1) return false;
        int[][] weights = {{5,4,3,2,9,8,7,6,5,4,3,2},{6,5,4,3,2,9,8,7,6,5,4,3,2}};
        for (int i=0; i<2; i++) {
            int sum=0;
            for (int j=0; j<weights[i].length; j++) sum+=(value.charAt(j)-'0')*weights[i][j];
            int remainder=sum%11;
            if (value.charAt(12+i)-'0' != (remainder<2?0:11-remainder)) return false;
        }
        return true;
    }
    public static void main(String[] args) throws Exception {
        if (args.length==1 && args[0].equals("--test")) {
            if (!assess(2,true,true,true,true).isEmpty()) throw new AssertionError();
            if (assess(8,false,true,true,true).size()!=2) throw new AssertionError();
            if (!validCnpj("00000000000191") || validCnpj("00000000000192")) throw new AssertionError();
            try {flag("yes");throw new AssertionError();} catch(IllegalArgumentException expected) {}
            System.out.println("4 registry policy checks passed"); return;
        }
        var input = new BufferedReader(new InputStreamReader(System.in));
        String cnpj=input.readLine();
        if (!validCnpj(cnpj)) throw new IllegalArgumentException("Invalid CNPJ");
        var issues=assess(Integer.parseInt(input.readLine()),flag(input.readLine()),flag(input.readLine()),flag(input.readLine()),flag(input.readLine()));
        var serialized=new ArrayList<String>();
        for (var code:issues) serialized.add("{\"code\":\""+code+"\",\"detail\":\"Registry evidence requires review\"}");
        System.out.println("{\"status\":\""+(issues.isEmpty()?"consistent":"review")+"\",\"issues\":["+String.join(",",serialized)+"],\"model\":\"registry-completeness-v1\",\"engine\":\"java\",\"notice\":\"Registry consistency is not a credit, fraud or compliance approval\"}");
    }
}
